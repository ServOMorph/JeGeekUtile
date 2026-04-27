import os
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
from config import config
from backend.models import db
from backend.auth import auth_bp
from backend.routes import main_bp
import logging

load_dotenv()

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    setup_logging(app)

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
    app.run(debug=True, host='127.0.0.1', port=5000)
