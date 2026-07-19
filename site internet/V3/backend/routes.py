from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from backend.models import db, User, PasswordReset, App
from backend.auth import login_required, admin_required
from backend.security import csrf_protect
from backend.services.email import EmailService
import logging

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__, url_prefix='')


@main_bp.route('/', methods=['GET'])
def index():
    if session.get('user_id'):
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        csrf_error = csrf_protect()
        if csrf_error:
            return csrf_error
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Email et mot de passe requis', 'error')
            return render_template('login.html'), 200

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Email ou mot de passe invalide', 'error')
            return render_template('login.html'), 200

        if not user.is_active:
            flash('Compte désactivé', 'error')
            return render_template('login.html'), 200

        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_role'] = user.role
        user.last_login = __import__('datetime').datetime.utcnow()
        db.session.commit()

        logger.info(f'User logged in: {email}')
        flash('Connexion réussie !', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@main_bp.route('/logout', methods=['POST'])
def logout():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))

    csrf_error = csrf_protect()
    if csrf_error:
        return csrf_error
    session.clear()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('main.login'))


@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        csrf_error = csrf_protect()
        if csrf_error:
            return csrf_error
        email = request.form.get('email', '').strip()

        if not email:
            flash('Email requis', 'error')
            return render_template('forgot_password.html'), 200

        user = User.query.filter_by(email=email).first()

        if user:
            success = EmailService.send_password_reset_email(email)
            if not success:
                logger.warning(f'Failed to send reset email to {email}')

        flash('Si cet email existe, un lien de réinitialisation y a été envoyé.', 'success')
        return render_template('forgot_password.html'), 200

    return render_template('forgot_password.html')


@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset = PasswordReset.query.filter_by(token=token).first()

    if not reset:
        flash('Lien de réinitialisation invalide', 'error')
        return render_template('error.html', code=404, message='Token invalide'), 404

    if not reset.is_valid():
        flash('Lien expiré ou déjà utilisé', 'error')
        return render_template('error.html', code=410, message='Token expiré'), 410

    if request.method == 'POST':
        csrf_error = csrf_protect()
        if csrf_error:
            return csrf_error
        new_password = request.form.get('password', '').strip()
        password_confirm = request.form.get('password_confirm', '').strip()

        if not new_password or not password_confirm:
            flash('Tous les champs sont requis', 'error')
            return render_template('reset_password.html', token=token), 200

        if new_password != password_confirm:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('reset_password.html', token=token), 200

        if len(new_password) < 8:
            flash('Le mot de passe doit contenir au moins 8 caractères', 'error')
            return render_template('reset_password.html', token=token), 200

        user = reset.user
        user.set_password(new_password)
        reset.mark_used()

        try:
            db.session.commit()
            EmailService.send_password_reset_confirmation(user.email)
            logger.info(f'Password reset successful for user {user.id}')
            flash('Mot de passe réinitialisé avec succès ! Connecte-toi.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Password reset failed for token {token}: {str(e)}')
            flash('Erreur lors de la réinitialisation', 'error')
            return render_template('reset_password.html', token=token), 500

    return render_template('reset_password.html', token=token)


@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = db.session.get(User, session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('main.login'))

    all_apps = App.query.filter_by(admin_only=False).all()
    installed_app_ids = set(user.installed_apps) if user.installed_apps else set()

    installed_apps = [app for app in all_apps if app.id in installed_app_ids]
    catalog_apps = [app for app in all_apps if app.id not in installed_app_ids]

    return render_template('dashboard.html', user=user, installed_apps=installed_apps, catalog_apps=catalog_apps)


@main_bp.route('/admin', methods=['GET'])
@admin_required
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)


@main_bp.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', code=404, message='Page non trouvée'), 404


@main_bp.errorhandler(403)
def page_forbidden(error):
    return render_template('error.html', code=403, message='Accès refusé'), 403


@main_bp.errorhandler(500)
def server_error(error):
    return render_template('error.html', code=500, message='Erreur serveur'), 500
