import pytest
import json
from datetime import datetime, timedelta
from app import create_app
from backend.models import db, User, PasswordReset


def set_csrf_token(client, value='test-csrf-token'):
    with client.session_transaction() as session:
        session['_csrf_token'] = value
    return value


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
    user = User(email='test@example.com')
    user.set_password('SecurePassword123')
    db.session.add(user)
    db.session.commit()
    return user


class TestUserRegistration:

    def test_register_success(self, client):
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'SecurePassword123'
        })
        assert response.status_code == 201
        assert response.json['email'] == 'newuser@example.com'

    def test_register_missing_email(self, client):
        response = client.post('/auth/register', json={
            'password': 'SecurePassword123'
        })
        assert response.status_code == 400
        assert 'Email et mot de passe requis' in response.json['error']

    def test_register_missing_password(self, client):
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com'
        })
        assert response.status_code == 400
        assert 'Email et mot de passe requis' in response.json['error']

    def test_register_duplicate_email(self, client, auth_user):
        response = client.post('/auth/register', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        assert response.status_code == 409
        assert 'Email déjà utilisé' in response.json['error']

    def test_register_weak_password(self, client):
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'weak'
        })
        assert response.status_code == 400
        assert '8 caractères' in response.json['error']


class TestLogin:

    def test_login_success(self, client, auth_user):
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        assert response.status_code == 200
        assert response.json['email'] == 'test@example.com'
        assert response.json['id'] == auth_user.id

    def test_login_invalid_email(self, client):
        response = client.post('/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'SomePassword123'
        })
        assert response.status_code == 401
        assert 'invalide' in response.json['error']

    def test_login_invalid_password(self, client, auth_user):
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword123'
        })
        assert response.status_code == 401
        assert 'invalide' in response.json['error']

    def test_login_sets_session(self, client, auth_user):
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_updates_last_login(self, client, auth_user):
        old_login = auth_user.last_login
        client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        updated_user = db.session.get(User, auth_user.id)
        assert updated_user.last_login is not None
        assert updated_user.last_login > (old_login or datetime.min)


class TestLogout:

    def test_logout_success(self, client, auth_user):
        client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        csrf_token = set_csrf_token(client)
        response = client.post('/auth/logout', headers={'X-CSRF-Token': csrf_token})
        assert response.status_code == 200
        assert 'réussi' in response.json['message']

    def test_logout_without_login(self, client):
        response = client.post('/auth/logout')
        assert response.status_code == 401


class TestPasswordReset:

    def test_reset_password_request_valid_email(self, client, auth_user):
        response = client.post('/auth/reset_password', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 200
        assert 'lien de réinitialisation' in response.json['message']

        reset = PasswordReset.query.filter_by(user_id=auth_user.id).first()
        assert reset is not None
        assert not reset.used
        assert reset.is_valid()

    def test_reset_password_nonexistent_email(self, client):
        response = client.post('/auth/reset_password', json={
            'email': 'nonexistent@example.com'
        })
        assert response.status_code == 200

    def test_reset_password_missing_email(self, client):
        response = client.post('/auth/reset_password', json={})
        assert response.status_code == 400
        assert 'Email requis' in response.json['error']

    def test_reset_token_generation(self, app, auth_user):
        with app.app_context():
            reset = PasswordReset.create_token(auth_user.id, 1)
            assert reset.token is not None
            assert reset.user_id == auth_user.id
            assert not reset.used
            assert reset.is_valid()

    def test_reset_token_expiration(self, app, auth_user):
        with app.app_context():
            reset = PasswordReset(
                token='expired-token',
                user_id=auth_user.id,
                expires_at=datetime.utcnow() - timedelta(hours=1),
                used=False
            )
            assert not reset.is_valid()

    def test_reset_token_used(self, app, auth_user):
        with app.app_context():
            reset = PasswordReset.create_token(auth_user.id, 1)
            reset.mark_used()
            assert not reset.is_valid()

    def test_confirm_reset_valid_token(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        response = client.post('/auth/confirm_reset', json={
            'token': reset.token,
            'password': 'NewPassword123'
        })
        assert response.status_code == 200
        assert 'mot de passe' in response.json['message'].lower()

        reset_after = PasswordReset.query.filter_by(token=reset.token).first()
        assert reset_after.used

        user_after = db.session.get(User, auth_user.id)
        assert user_after.check_password('NewPassword123')

    def test_confirm_reset_invalid_token(self, client):
        response = client.post('/auth/confirm_reset', json={
            'token': 'invalid-token',
            'password': 'NewPassword123'
        })
        assert response.status_code == 404
        assert 'invalide' in response.json['error']

    def test_confirm_reset_expired_token(self, client, auth_user):
        reset = PasswordReset(
            token='expired-token',
            user_id=auth_user.id,
            expires_at=datetime.utcnow() - timedelta(hours=1),
            used=False
        )
        db.session.add(reset)
        db.session.commit()

        response = client.post('/auth/confirm_reset', json={
            'token': 'expired-token',
            'password': 'NewPassword123'
        })
        assert response.status_code == 410

    def test_confirm_reset_already_used_token(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        reset.mark_used()
        db.session.add(reset)
        db.session.commit()

        response = client.post('/auth/confirm_reset', json={
            'token': reset.token,
            'password': 'NewPassword123'
        })
        assert response.status_code == 410

    def test_confirm_reset_weak_password(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        response = client.post('/auth/confirm_reset', json={
            'token': reset.token,
            'password': 'weak'
        })
        assert response.status_code == 400
        assert '8 caractères' in response.json['error']

    def test_verify_token_valid(self, client, auth_user):
        reset = PasswordReset.create_token(auth_user.id, 1)
        db.session.add(reset)
        db.session.commit()

        response = client.get(f'/auth/verify_token/{reset.token}')
        assert response.status_code == 200
        assert response.json['valid'] is True
        assert response.json['user_email'] == auth_user.email

    def test_verify_token_invalid(self, client):
        response = client.get('/auth/verify_token/invalid-token')
        assert response.status_code == 404
        assert response.json['valid'] is False

    def test_verify_token_expired(self, client, auth_user):
        reset = PasswordReset(
            token='expired-token',
            user_id=auth_user.id,
            expires_at=datetime.utcnow() - timedelta(hours=1),
            used=False
        )
        db.session.add(reset)
        db.session.commit()

        response = client.get('/auth/verify_token/expired-token')
        assert response.status_code == 410
        assert response.json['valid'] is False


class TestCurrentUser:

    def test_get_current_user_success(self, client, auth_user):
        client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        response = client.get('/auth/me')
        assert response.status_code == 200
        assert response.json['email'] == 'test@example.com'
        assert response.json['role'] == 'user'

    def test_get_current_user_not_logged_in(self, client):
        response = client.get('/auth/me')
        assert response.status_code == 401

    def test_get_current_user_not_found(self, client, auth_user):
        client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        User.query.filter_by(id=auth_user.id).delete()
        db.session.commit()
        response = client.get('/auth/me')
        assert response.status_code == 404


class TestPasswordResetFlow10Steps:
    """
    Processus complet reset MDP en 10 étapes :
    1. Utilisateur clique "Mot de passe oublié"
    2. Saisit email
    3. Envoi email avec token
    4. Clic lien dans email / Vérification token
    5. Affichage formulaire nouveau MDP
    6. Saisie + validation nouveau MDP
    7. Validation token (non expiré, non utilisé)
    8. Update password_hash en DB
    9. Marquer token comme "used"
    10. Confirmation / Login avec nouveau MDP
    """

    def test_complete_password_reset_flow(self, client, auth_user):
        original_password_hash = auth_user.password_hash

        step1 = "Utilisateur clique mot de passe oublié"
        step2 = "Utilisateur saisit email"
        response = client.post('/auth/reset_password', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 200

        reset = PasswordReset.query.filter_by(user_id=auth_user.id).first()
        assert reset is not None
        token = reset.token

        step4 = "Vérifier token"
        response = client.get(f'/auth/verify_token/{token}')
        assert response.status_code == 200
        assert response.json['valid'] is True

        step6_7 = "Utilisateur soumet nouveau MDP avec token valide"
        response = client.post('/auth/confirm_reset', json={
            'token': token,
            'password': 'CompletelyNewPassword456'
        })
        assert response.status_code == 200

        step8_9 = "Vérifier que password_hash est changé et token marqué used"
        user_updated = db.session.get(User, auth_user.id)
        assert user_updated.password_hash != original_password_hash
        assert user_updated.check_password('CompletelyNewPassword456')

        reset_used = PasswordReset.query.filter_by(token=token).first()
        assert reset_used.used

        step10 = "Tenter connexion avec nouveau MDP"
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'CompletelyNewPassword456'
        })
        assert response.status_code == 200
        assert response.json['email'] == 'test@example.com'

        step10_old_password = "Ancien MDP ne fonctionne plus"
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        })
        assert response.status_code == 401
