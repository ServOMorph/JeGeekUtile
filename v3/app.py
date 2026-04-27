import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from dotenv import load_dotenv
from config import config
from backend.models import db, User, App
from backend.auth import auth_bp
from backend.routes import main_bp
from backend.apps import apps_bp
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

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        _create_test_users()

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(apps_bp)

    setup_logging(app)

    bot_assets_dir = r'D:\ServOMorph\Bot ou pas Bot\UI\V3\ASSETS'
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
        from backend.models import User
        from flask import session
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                # Logic for progression (placeholder for now)
                # In Phase 8 we will implement real tracking
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
        import markdown
        content = {}
        
        # Presentation
        pres_path = os.path.join(base_dir, 'src', 'content', 'presentation.md')
        try:
            if os.path.exists(pres_path):
                with open(pres_path, 'r', encoding='utf-8') as f:
                    content['presentation_html'] = markdown.markdown(f.read(), extensions=['extra', 'admonition', 'codehilite'])
        except Exception as e:
            app.logger.error(f"Error loading presentation.md: {e}")
            content['presentation_html'] = '<p>Erreur de chargement.</p>'

        # Projects
        proj_path = os.path.join(base_dir, 'src', 'content', 'projects.md')
        try:
            if os.path.exists(proj_path):
                with open(proj_path, 'r', encoding='utf-8') as f:
                    content['projects_html'] = markdown.markdown(f.read(), extensions=['extra', 'admonition', 'codehilite'])
        except Exception as e:
            app.logger.error(f"Error loading projects.md: {e}")
            content['projects_html'] = '<p>Erreur de chargement.</p>'

        return content

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


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
