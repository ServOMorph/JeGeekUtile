from flask import Blueprint, request, jsonify, session
from backend.models import db, User, PasswordReset
from backend.services.email import EmailService
from backend.security import csrf_protect, rate_limit
from datetime import datetime
from functools import wraps
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        user = db.session.get(User, session['user_id'])
        if not user or user.role != 'admin':
            return jsonify({'error': 'Forbidden'}), 403
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['POST'])
@rate_limit('auth-register', 10, 300)
def register():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email et mot de passe requis'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409

    if len(password) < 8:
        return jsonify({'error': 'Le mot de passe doit contenir au moins 8 caractères'}), 400

    user = User(email=email)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        logger.info(f'New user registered: {email}')
        return jsonify({'id': user.id, 'email': user.email}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f'Registration failed for {email}: {str(e)}')
        return jsonify({'error': 'Erreur lors de l\'inscription'}), 500


@auth_bp.route('/login', methods=['POST'])
@rate_limit('auth-login', 'LOGIN_RATE_LIMIT_MAX', 'LOGIN_RATE_LIMIT_WINDOW')
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email et mot de passe requis'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Email ou mot de passe invalide'}), 401

    if not user.is_active:
        return jsonify({'error': 'Compte désactivé'}), 403

    session['user_id'] = user.id
    session['user_email'] = user.email
    session['user_role'] = user.role
    user.last_login = datetime.utcnow()
    db.session.commit()

    logger.info(f'User logged in: {email}')
    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    csrf_error = csrf_protect()
    if csrf_error:
        return csrf_error
    user_id = session.get('user_id')
    session.clear()
    logger.info(f'User logged out: {user_id}')
    return jsonify({'message': 'Déconnexion réussie'}), 200


@auth_bp.route('/reset_password', methods=['POST'])
@rate_limit('auth-reset', 'RESET_RATE_LIMIT_MAX', 'RESET_RATE_LIMIT_WINDOW')
def reset_password():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()

    if not email:
        return jsonify({'error': 'Email requis'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'}), 200

    success = EmailService.send_password_reset_email(email)

    if not success:
        logger.warning(f'Failed to send reset email to {email}')
        return jsonify({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'}), 200

    return jsonify({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'}), 200


@auth_bp.route('/confirm_reset', methods=['POST'])
@rate_limit('auth-confirm-reset', 10, 300)
def confirm_reset():
    data = request.get_json(silent=True) or {}
    token = data.get('token', '').strip()
    new_password = data.get('password', '').strip()

    if not token or not new_password:
        return jsonify({'error': 'Token et mot de passe requis'}), 400

    if len(new_password) < 8:
        return jsonify({'error': 'Le mot de passe doit contenir au moins 8 caractères'}), 400

    reset = PasswordReset.query.filter_by(token=token).first()

    if not reset:
        return jsonify({'error': 'Token invalide'}), 404

    if not reset.is_valid():
        return jsonify({'error': 'Token expiré ou déjà utilisé'}), 410

    user = reset.user
    user.set_password(new_password)
    reset.mark_used()

    try:
        db.session.commit()
        EmailService.send_password_reset_confirmation(user.email)
        logger.info(f'Password reset successful for user {user.id}')
        return jsonify({'message': 'Mot de passe réinitialisé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Password reset failed for token {token}: {str(e)}')
        return jsonify({'error': 'Erreur lors de la réinitialisation'}), 500


@auth_bp.route('/verify_token/<token>', methods=['GET'])
def verify_token(token):
    reset = PasswordReset.query.filter_by(token=token).first()

    if not reset:
        return jsonify({'valid': False, 'error': 'Token invalide'}), 404

    if reset.is_valid():
        return jsonify({'valid': True, 'user_email': reset.user.email}), 200
    return jsonify({'valid': False, 'error': 'Token expiré ou déjà utilisé'}), 410


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    user = db.session.get(User, session['user_id'])
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    return jsonify(user.to_dict()), 200
