import pytest
from app import create_app
from backend.models import db, User, PasswordReset
from datetime import datetime, timedelta


def prime_csrf(client, path='/login'):
    client.get(path)
    with client.session_transaction() as session:
        return session['_csrf_token']


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_user(app):
    user = User(email='test@example.com', role='user')
    user.set_password('SecurePassword123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def admin_user(app):
    user = User(email='admin@example.com', role='admin')
    user.set_password('AdminPassword123')
    db.session.add(user)
    db.session.commit()
    return user


class TestIndex:

    def test_index_redirect_to_login_not_authenticated(self, client):
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location

    def test_index_redirect_to_dashboard_authenticated(self, client, auth_user):
        csrf_token = prime_csrf(client)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/dashboard' in response.location


class TestLogin:

    def test_login_page_get(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert b'LOGIN' in response.data

    def test_login_success(self, client, auth_user):
        csrf_token = prime_csrf(client)
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        }, follow_redirects=False)
        assert response.status_code == 302
        assert '/dashboard' in response.location

    def test_login_invalid_email(self, client):
        csrf_token = prime_csrf(client)
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'SomePassword123',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200
        assert b'invalide' in response.data

    def test_login_invalid_password(self, client, auth_user):
        csrf_token = prime_csrf(client)
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPassword123',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200
        assert b'invalide' in response.data

    def test_login_missing_email(self, client):
        csrf_token = prime_csrf(client)
        response = client.post('/login', data={
            'password': 'SomePassword123',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200
        assert b'LOGIN' in response.data

    def test_login_sets_session(self, client, auth_user):
        csrf_token = prime_csrf(client)
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        assert response.status_code == 302

    def test_login_inactive_user(self, client, auth_user):
        auth_user.is_active = False
        db.session.commit()

        csrf_token = prime_csrf(client)
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200


class TestLogout:

    def test_logout_success(self, client, auth_user):
        login_csrf = prime_csrf(client)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': login_csrf
        })
        logout_csrf = prime_csrf(client, '/dashboard')
        response = client.post('/logout', data={'csrf_token': logout_csrf}, follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location

    def test_logout_without_login(self, client):
        response = client.post('/logout', follow_redirects=False)
        assert response.status_code == 302


class TestForgotPassword:

    def test_forgot_password_page_get(self, client):
        response = client.get('/forgot-password')
        assert response.status_code == 200
        assert b'RESET MDP' in response.data

    def test_forgot_password_valid_email(self, client, auth_user):
        csrf_token = prime_csrf(client, '/forgot-password')
        response = client.post('/forgot-password', data={
            'email': 'test@example.com',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200
        assert b'envoy' in response.data.lower() or b'lien' in response.data.lower()

        reset = PasswordReset.query.filter_by(user_id=auth_user.id).first()
        assert reset is not None

    def test_forgot_password_nonexistent_email(self, client):
        csrf_token = prime_csrf(client, '/forgot-password')
        response = client.post('/forgot-password', data={
            'email': 'nonexistent@example.com',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200

    def test_forgot_password_missing_email(self, client):
        csrf_token = prime_csrf(client, '/forgot-password')
        response = client.post('/forgot-password', data={'csrf_token': csrf_token})
        assert response.status_code == 200


class TestResetPassword:

    def test_reset_password_valid_token(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        response = client.get(f'/reset-password/{reset.token}')
        assert response.status_code == 200
        assert b'NOUVEAU MDP' in response.data

    def test_reset_password_invalid_token(self, client):
        response = client.get('/reset-password/invalid-token')
        assert response.status_code == 404

    def test_reset_password_expired_token(self, client, auth_user):
        reset = PasswordReset(
            token='expired-token',
            user_id=auth_user.id,
            expires_at=datetime.utcnow() - timedelta(hours=1),
            used=False
        )
        db.session.add(reset)
        db.session.commit()

        response = client.get('/reset-password/expired-token')
        assert response.status_code == 410

    def test_reset_password_post_success(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        csrf_token = prime_csrf(client, f'/reset-password/{reset.token}')
        response = client.post(f'/reset-password/{reset.token}', data={
            'password': 'NewPassword123',
            'password_confirm': 'NewPassword123',
            'csrf_token': csrf_token
        }, follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location

    def test_reset_password_post_mismatch(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        csrf_token = prime_csrf(client, f'/reset-password/{reset.token}')
        response = client.post(f'/reset-password/{reset.token}', data={
            'password': 'NewPassword123',
            'password_confirm': 'DifferentPassword456',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200

    def test_reset_password_post_weak_password(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        csrf_token = prime_csrf(client, f'/reset-password/{reset.token}')
        response = client.post(f'/reset-password/{reset.token}', data={
            'password': 'weak',
            'password_confirm': 'weak',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200


class TestDashboard:

    def test_dashboard_authenticated(self, client, auth_user):
        csrf_token = prime_csrf(client)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'DASHBOARD' in response.data

    def test_dashboard_not_authenticated(self, client):
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 401

    def test_dashboard_deleted_user(self, client, auth_user):
        csrf_token = prime_csrf(client)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        User.query.filter_by(id=auth_user.id).delete()
        db.session.commit()

        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302


class TestAdmin:

    def test_admin_authenticated_admin(self, client, admin_user):
        csrf_token = prime_csrf(client)
        client.post('/login', data={
            'email': 'admin@example.com',
            'password': 'AdminPassword123',
            'csrf_token': csrf_token
        })
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'PANEL ADMIN' in response.data or b'Panel Admin' in response.data

    def test_admin_not_authenticated(self, client):
        response = client.get('/admin', follow_redirects=False)
        assert response.status_code == 401

    def test_admin_authenticated_non_admin(self, client, auth_user):
        csrf_token = prime_csrf(client)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        response = client.get('/admin', follow_redirects=False)
        assert response.status_code == 403


class TestErrorPages:

    def test_404_error(self, client):
        response = client.get('/nonexistent-page')
        assert response.status_code == 404

    def test_403_error(self, client, auth_user):
        csrf_token = prime_csrf(client)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123',
            'csrf_token': csrf_token
        })
        response = client.get('/admin')
        assert response.status_code == 403
