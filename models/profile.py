from __future__ import unicode_literals

import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

ROLES = {'admin': 'admin', 'operator': 'operator', 'visitor': 'visitor', }


class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, required=True)
    password_hash = db.StringField(required=True)
    nick_name = db.StringField(max_length=255, default=str(username))
    email = db.EmailField(max_length=255)
    biography = db.StringField()
    url = db.URLField()
    date_created = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    last_login = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    role = db.StringField(max_length=32, default='admin', choices=ROLES)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def __unicode__(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user
