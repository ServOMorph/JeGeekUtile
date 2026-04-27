from flask import Blueprint, request, jsonify, session
from backend.models import db, User, App
from backend.auth import login_required
import logging

logger = logging.getLogger(__name__)

apps_bp = Blueprint('apps', __name__, url_prefix='/api/apps')

@apps_bp.route('/catalog', methods=['GET'])
@login_required
def get_catalog():
    apps = App.query.filter_by(admin_only=False).all()
    return jsonify([app.to_dict() for app in apps]), 200

@apps_bp.route('/install', methods=['POST'])
@login_required
def install_app():
    data = request.get_json()
    app_id = data.get('app_id')
    
    if not app_id:
        return jsonify({'success': False, 'message': 'ID d\'application requis'}), 400
        
    user = User.query.get(session['user_id'])
    app = App.query.get(app_id)
    
    if not app:
        return jsonify({'success': False, 'message': 'Application non trouvée'}), 404
        
    if user.installed_apps is None:
        user.installed_apps = []
        
    if app_id in user.installed_apps:
        return jsonify({'success': False, 'message': 'Application déjà installée'}), 400
        
    # We need to make a copy of the list to trigger SQLAlchemy change detection for JSON column
    new_installed_apps = list(user.installed_apps)
    new_installed_apps.append(app_id)
    user.installed_apps = new_installed_apps
    
    try:
        db.session.commit()
        logger.info(f'App {app.slug} installed for user {user.id}')
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Failed to install app {app_id} for user {user.id}: {str(e)}')
        return jsonify({'success': False, 'message': 'Erreur lors de l\'installation'}), 500

@apps_bp.route('/uninstall', methods=['DELETE'])
@login_required
def uninstall_app():
    data = request.get_json()
    app_id = data.get('app_id')
    
    if not app_id:
        return jsonify({'success': False, 'message': 'ID d\'application requis'}), 400
        
    user = User.query.get(session['user_id'])
    app = App.query.get(app_id)
    
    if not app:
        return jsonify({'success': False, 'message': 'Application non trouvée'}), 404
        
    if app.is_default:
        return jsonify({'success': False, 'message': 'Impossible de désinstaller une application par défaut'}), 400
        
    if not user.installed_apps or app_id not in user.installed_apps:
        return jsonify({'success': False, 'message': 'Application non installée'}), 400
        
    new_installed_apps = list(user.installed_apps)
    new_installed_apps.remove(app_id)
    user.installed_apps = new_installed_apps
    
    try:
        db.session.commit()
        logger.info(f'App {app.slug} uninstalled for user {user.id}')
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Failed to uninstall app {app_id} for user {user.id}: {str(e)}')
        return jsonify({'success': False, 'message': 'Erreur lors de la désinstallation'}), 500
