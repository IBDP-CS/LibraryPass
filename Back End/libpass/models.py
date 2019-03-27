from flask_login import UserMixin
from werkzeug.security import check_password_hash

from libpass import db, login_manager


class User(UserMixin, db.Model):
    '''Model for the users table.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.String(60), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_student = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def authenticate(self, password):
        '''Checks if provided password matches hashed password.'''
        return check_password_hash(self.password, password)


class State(db.Model):
    '''Model for the states table.'''

    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.String(60), db.ForeignKey('users.school_id'), nullable=False)
    state = db.Column(db.Integer, nullable=False, default=0)
