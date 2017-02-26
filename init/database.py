# Stdlib imports

# Core Flask imports

# Third-party app imports
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

# Imports from your apps


db = SQLAlchemy()


class BaseModel(object):
    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True)


class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=func.now(), nullable=False)


class UserMixin(object):
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    @declared_attr
    def user(cls):
        return db.relationship('User')
