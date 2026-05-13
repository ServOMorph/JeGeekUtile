import pytest
from app import create_app
from backend.models import db, User, App


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
    user = User(email='test@example.com', role='user', installed_apps=[])
    user.set_password('SecurePassword123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def login(client, auth_user):
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'SecurePassword123'
    })
    assert response.status_code == 200
    return auth_user


@pytest.fixture
def public_app(app):
    test_app = App(
        name='Presentation',
        slug='presentation',
        html_path='/apps/presentation/index.html',
        description='Public app',
        version='1.0.0',
        is_default=False,
        admin_only=False
    )
    db.session.add(test_app)
    db.session.commit()
    return test_app


@pytest.fixture
def default_app(app):
    test_app = App(
        name='Core',
        slug='core',
        html_path='/apps/core/index.html',
        description='Default app',
        version='1.0.0',
        is_default=True,
        admin_only=False
    )
    db.session.add(test_app)
    db.session.commit()
    return test_app


@pytest.fixture
def admin_only_app(app):
    test_app = App(
        name='Admin',
        slug='admin-tools',
        html_path='/apps/admin/index.html',
        description='Admin app',
        version='1.0.0',
        is_default=False,
        admin_only=True
    )
    db.session.add(test_app)
    db.session.commit()
    return test_app


class TestAppCatalog:

    def test_catalog_requires_login(self, client):
        response = client.get('/api/apps/catalog')
        assert response.status_code == 401

    def test_catalog_returns_only_public_apps(self, client, login, public_app, admin_only_app):
        response = client.get('/api/apps/catalog')
        assert response.status_code == 200
        payload = response.get_json()
        assert len(payload) == 1
        assert payload[0]['slug'] == 'presentation'


class TestAppInstall:

    def test_install_requires_login(self, client):
        response = client.post('/api/apps/install', json={'app_id': 1})
        assert response.status_code == 401

    def test_install_missing_app_id(self, client, login):
        response = client.post('/api/apps/install', json={})
        assert response.status_code == 400
        assert response.get_json()['success'] is False

    def test_install_unknown_app(self, client, login):
        response = client.post('/api/apps/install', json={'app_id': 999})
        assert response.status_code == 404
        assert response.get_json()['success'] is False

    def test_install_success(self, client, login, auth_user, public_app):
        response = client.post('/api/apps/install', json={'app_id': public_app.id})
        assert response.status_code == 200
        assert response.get_json()['success'] is True

        db.session.refresh(auth_user)
        assert public_app.id in auth_user.installed_apps

    def test_install_already_installed(self, client, login, auth_user, public_app):
        auth_user.installed_apps = [public_app.id]
        db.session.commit()

        response = client.post('/api/apps/install', json={'app_id': public_app.id})
        assert response.status_code == 400
        assert response.get_json()['success'] is False

    def test_install_commit_failure(self, client, login, auth_user, public_app, monkeypatch):
        def fail_commit():
            raise Exception('db failure')

        monkeypatch.setattr(db.session, 'commit', fail_commit)

        response = client.post('/api/apps/install', json={'app_id': public_app.id})
        assert response.status_code == 500
        assert response.get_json()['success'] is False


class TestAppUninstall:

    def test_uninstall_requires_login(self, client):
        response = client.delete('/api/apps/uninstall', json={'app_id': 1})
        assert response.status_code == 401

    def test_uninstall_missing_app_id(self, client, login):
        response = client.delete('/api/apps/uninstall', json={})
        assert response.status_code == 400
        assert response.get_json()['success'] is False

    def test_uninstall_unknown_app(self, client, login):
        response = client.delete('/api/apps/uninstall', json={'app_id': 999})
        assert response.status_code == 404
        assert response.get_json()['success'] is False

    def test_uninstall_default_app_forbidden(self, client, login, auth_user, default_app):
        auth_user.installed_apps = [default_app.id]
        db.session.commit()

        response = client.delete('/api/apps/uninstall', json={'app_id': default_app.id})
        assert response.status_code == 400
        assert response.get_json()['success'] is False

    def test_uninstall_not_installed(self, client, login, public_app):
        response = client.delete('/api/apps/uninstall', json={'app_id': public_app.id})
        assert response.status_code == 400
        assert response.get_json()['success'] is False

    def test_uninstall_success(self, client, login, auth_user, public_app):
        auth_user.installed_apps = [public_app.id]
        db.session.commit()

        response = client.delete('/api/apps/uninstall', json={'app_id': public_app.id})
        assert response.status_code == 200
        assert response.get_json()['success'] is True

        db.session.refresh(auth_user)
        assert public_app.id not in auth_user.installed_apps

    def test_uninstall_commit_failure(self, client, login, auth_user, public_app, monkeypatch):
        auth_user.installed_apps = [public_app.id]
        db.session.commit()

        def fail_commit():
            raise Exception('db failure')

        monkeypatch.setattr(db.session, 'commit', fail_commit)

        response = client.delete('/api/apps/uninstall', json={'app_id': public_app.id})
        assert response.status_code == 500
        assert response.get_json()['success'] is False
