from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    progress_json = db.Column(db.JSON, default=dict, nullable=False)
    installed_apps = db.Column(db.JSON, default=list, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    password_resets = db.relationship('PasswordReset', back_populates='user', cascade='all, delete-orphan')
    app_data = db.relationship('AppData', back_populates='user', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_password=False):
        data = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
        if not include_password:
            return data
        return data

    def __repr__(self):
        return f'<User {self.email}>'


class App(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    html_path = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512), default='', nullable=False)
    version = db.Column(db.String(50), default='1.0.0', nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    admin_only = db.Column(db.Boolean, default=False, nullable=False)
    icon = db.Column(db.String(255), default='', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    app_data = db.relationship('AppData', back_populates='app', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'version': self.version,
            'is_default': self.is_default,
            'admin_only': self.admin_only,
            'icon': self.icon
        }

    def __repr__(self):
        return f'<App {self.slug}>'


class AppData(db.Model):
    __tablename__ = 'app_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False, index=True)
    data_json = db.Column(db.JSON, default=dict, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='app_data')
    app = db.relationship('App', back_populates='app_data')

    __table_args__ = (db.UniqueConstraint('user_id', 'app_id', name='uq_user_app'),)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'app_id': self.app_id,
            'data': self.data_json,
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<AppData user_id={self.user_id} app_id={self.app_id}>'


class Config(db.Model):
    __tablename__ = 'config'

    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(5000), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {'key': self.key, 'value': self.value}

    def __repr__(self):
        return f'<Config {self.key}>'


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = db.relationship('User', back_populates='messages')

    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }

    def __repr__(self):
        return f'<Message chat_id={self.chat_id} user_id={self.user_id}>'


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    token = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='password_resets')

    @staticmethod
    def create_token(user_id, expiry_hours=1):
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=expiry_hours)
        reset = PasswordReset(token=token, user_id=user_id, expires_at=expires_at)
        return reset

    def is_valid(self):
        return not self.used and datetime.utcnow() < self.expires_at

    def mark_used(self):
        self.used = True

    def to_dict(self):
        return {
            'token': self.token,
            'user_id': self.user_id,
            'expires_at': self.expires_at.isoformat(),
            'used': self.used
        }

    def __repr__(self):
        return f'<PasswordReset user_id={self.user_id} valid={self.is_valid()}>'
