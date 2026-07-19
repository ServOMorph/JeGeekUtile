import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, url_for
from backend.models import db, User, PasswordReset
import logging

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(to_email, subject, html_content, text_content=None):
        try:
            smtp_server = current_app.config['SMTP_SERVER']
            smtp_port = current_app.config['SMTP_PORT']
            smtp_username = current_app.config['SMTP_USERNAME']
            smtp_password = current_app.config['SMTP_PASSWORD']
            from_email = current_app.config['SMTP_FROM_EMAIL']

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email

            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))

            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            logger.info(f'Email sent successfully to {to_email}')
            return True
        except Exception as e:
            logger.error(f'Failed to send email to {to_email}: {str(e)}')
            return False

    @staticmethod
    def send_password_reset_email(user_email):
        user = User.query.filter_by(email=user_email).first()
        if not user:
            logger.warning(f'Password reset requested for non-existent user: {user_email}')
            return True

        reset = PasswordReset.create_token(
            user.id,
            current_app.config['PASSWORD_RESET_EXPIRY_HOURS']
        )
        db.session.add(reset)
        db.session.commit()

        reset_url = url_for('main.reset_password', token=reset.token, _external=True)

        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #1a1a1a; color: #b8b8b8;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #2a2a2a; border-radius: 8px;">
                    <h2 style="color: #6b8e23;">Réinitialisation de mot de passe</h2>
                    <p>Bonjour,</p>
                    <p>Vous avez demandé une réinitialisation de votre mot de passe.
                    Cliquez sur le lien ci-dessous pour continuer :</p>
                    <p style="margin: 30px 0;">
                        <a href="{reset_url}" style="background-color: #2d5016; color: #b8b8b8; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">
                            Réinitialiser mon mot de passe
                        </a>
                    </p>
                    <p style="font-size: 12px; color: #888;">
                        Ce lien expirera dans {current_app.config['PASSWORD_RESET_EXPIRY_HOURS']} heure(s).
                    </p>
                    <p style="font-size: 12px; color: #888;">
                        Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
                    </p>
                    <hr style="border: none; border-top: 1px solid #444; margin: 20px 0;">
                    <p style="font-size: 11px; color: #666;">
                        JeGeekUtile — La technologie au service de l'humain
                    </p>
                </div>
            </body>
        </html>
        """

        text_content = f"""
Réinitialisation de mot de passe

Bonjour,

Vous avez demandé une réinitialisation de votre mot de passe.
Cliquez sur le lien ci-dessous pour continuer :

{reset_url}

Ce lien expirera dans {current_app.config['PASSWORD_RESET_EXPIRY_HOURS']} heure(s).

Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.

---
JeGeekUtile — La technologie au service de l'humain
        """

        subject = "Réinitialisation de votre mot de passe - JeGeekUtile"
        return EmailService.send_email(user_email, subject, html_content, text_content)

    @staticmethod
    def send_password_reset_confirmation(user_email):
        html_content = """
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #1a1a1a; color: #b8b8b8;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #2a2a2a; border-radius: 8px;">
                    <h2 style="color: #6b8e23;">Mot de passe réinitialisé</h2>
                    <p>Votre mot de passe a été réinitialisé avec succès.</p>
                    <p>Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.</p>
                    <p style="font-size: 12px; color: #888;">
                        Si vous n'avez pas effectué cette action, contactez un administrateur immédiatement.
                    </p>
                    <hr style="border: none; border-top: 1px solid #444; margin: 20px 0;">
                    <p style="font-size: 11px; color: #666;">
                        JeGeekUtile — La technologie au service de l'humain
                    </p>
                </div>
            </body>
        </html>
        """

        text_content = """
Mot de passe réinitialisé

Votre mot de passe a été réinitialisé avec succès.
Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.

Si vous n'avez pas effectué cette action, contactez un administrateur immédiatement.

---
JeGeekUtile — La technologie au service de l'humain
        """

        subject = "Confirmation de réinitialisation - JeGeekUtile"
        return EmailService.send_email(user_email, subject, html_content, text_content)
