import os
from pathlib import Path

import markdown
from flask import Flask, redirect, url_for, send_from_directory
from dotenv import load_dotenv
from config import config
from backend.models import db, User, App
from backend.auth import auth_bp
from backend.routes import main_bp
from backend.apps import apps_bp
from backend.security import get_csrf_token
import logging

load_dotenv()

def _create_test_users():
    test_email = 'test@example.com'
    admin_email = 'admin@example.com'

    test_user = User.query.filter_by(email=test_email).first()
    if not test_user:
        test_user = User(email=test_email, role='user')
        test_user.set_password('TestPassword123')
        db.session.add(test_user)
        db.session.commit()
        print(f'[OK] Test account created: {test_email} / TestPassword123')
    else:
        print(f'[INFO] Test account already exists: {test_email}')

    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(email=admin_email, role='admin')
        admin_user.set_password('AdminPassword123')
        db.session.add(admin_user)
        db.session.commit()
        print(f'[OK] Admin account created: {admin_email} / AdminPassword123')
    else:
        print(f'[INFO] Admin account already exists: {admin_email}')

    presentation_app = App.query.filter_by(slug='presentation').first()
    if not presentation_app:
        presentation_app = App(
            name='Présentation',
            slug='presentation',
            html_path='/apps/presentation/index.html',
            description='Découvrez le projet JeGeekUtile',
            version='1.0.0',
            is_default=True,
            admin_only=False
        )
        db.session.add(presentation_app)
        db.session.commit()
        print(f'[OK] App created: Présentation')

    if test_user and presentation_app and presentation_app.id not in (test_user.installed_apps or []):
        test_user.installed_apps = test_user.installed_apps or []
        test_user.installed_apps.append(presentation_app.id)
        db.session.commit()
        print(f'[OK] App installed for test user: Présentation')

    if admin_user and presentation_app and presentation_app.id not in (admin_user.installed_apps or []):
        admin_user.installed_apps = admin_user.installed_apps or []
        admin_user.installed_apps.append(presentation_app.id)
        db.session.commit()
        print(f'[OK] App installed for admin user: Présentation')

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'src', 'templates')
    static_dir = os.path.join(base_dir, 'src', 'static')

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path='/static',
        instance_relative_config=True
    )
    app.config.from_object(config[config_name])
    _validate_runtime_config(app)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        if app.config.get('BOOTSTRAP_TEST_USERS'):
            _create_test_users()

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(apps_bp)

    setup_logging(app)

    bot_assets_dir = r'D:\ServOMorph\Bot ou pas Bot\UI\V3\ASSETS'
    content_cache = {}

    @app.route('/apps/<path:filename>')
    def serve_apps(filename):
        apps_dir = os.path.join(base_dir, 'src', 'apps')
        return send_from_directory(apps_dir, filename)

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        if os.path.exists(bot_assets_dir):
            return send_from_directory(bot_assets_dir, filename)
        return {'error': 'Asset not found'}, 404

    @app.context_processor
    def inject_progression():
        from flask import session
        user_id = session.get('user_id')
        if user_id:
            return {
                'progression': {
                    'level': 12,
                    'percent': 65,
                    'geekos': 1250
                }
            }
        return {'progression': None}

    @app.context_processor
    def inject_content():
        return {
            'presentation_html': _render_markdown_content(app, content_cache, Path(base_dir) / 'src' / 'content' / 'presentation.md'),
            'projects_html': _render_markdown_content(app, content_cache, Path(base_dir) / 'src' / 'content' / 'projects.md'),
            'csrf_token': get_csrf_token(),
        }

    @app.route('/')
    def index():
        return redirect(url_for('auth.get_current_user'))

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal server error'}, 500

    return app


def setup_logging(app):
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.FileHandler('logs/jegeekutile.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('JeGeekUtile V3 startup')


def _validate_runtime_config(app):
    if app.config.get('TESTING'):
        return

    if app.config.get('SECRET_KEY') == 'dev-secret-key-change-in-prod':
        app.logger.warning('SECRET_KEY par défaut détectée; remplace-la avant mise en production.')

    if app.config.get('PASSWORD_RESET_SALT') == 'reset-salt-change-in-prod':
        app.logger.warning('PASSWORD_RESET_SALT par défaut détecté; remplace-le avant mise en production.')


def _render_markdown_content(app, cache, path):
    cache_key = str(path)

    try:
        if not path.exists():
            return '<p>Contenu indisponible.</p>'

        mtime = path.stat().st_mtime
        cached = cache.get(cache_key)
        if cached and cached['mtime'] == mtime:
            return cached['html']

        html = markdown.markdown(
            path.read_text(encoding='utf-8'),
            extensions=['extra', 'admonition', 'codehilite']
        )
        cache[cache_key] = {'mtime': mtime, 'html': html}
        return html
    except Exception as exc:
        app.logger.error(f'Error loading {path.name}: {exc}')
        return '<p>Erreur de chargement.</p>'


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
