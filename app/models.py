from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    discord_tag = db.Column(db.String(64), nullable=False)
    bio = db.Column(db.String(500), default="")
    is_admin = db.Column(db.Boolean, default=False)

    listings = db.relationship('Listing', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)

    listings = db.relationship('Listing', backref='game', lazy='dynamic')


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    rank = db.Column(db.String(50), nullable=False)  #желаемый ранг
    play_time = db.Column(db.String(50), nullable=False)  # утро день вечерь ночь, вообщем время суток
    voice_chat = db.Column(db.String(50), nullable=False)  # Discord, In-game и т.д.
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="active")  # active / closed и еще возможно
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)