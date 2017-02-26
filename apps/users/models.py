# Stdlib imports

# Core Flask imports

# Third-party app imports
from sqlalchemy import func

# Imports from your apps
from init.database import db, TimestampMixin, BaseModel

__all__ = (
    'User',
    'Invite'
)


class User(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'users'

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLES = (
        ROLE_USER,
        ROLE_ADMIN
    )

    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(80), default=ROLE_USER)

    allow_datetime = db.Column(
        db.DateTime, default=func.current_timestamp().op('AT TIME ZONE')('UTC'), nullable=False
    )
    active = db.Column(db.Boolean, default=True)

    avatar_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    avatar = db.relationship('File', foreign_keys=avatar_id)

    def __unicode__(self):
        return '{0}'.format(self.email)


class Invite(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'invites'

    TYPE_INTERNAL = 'internal'
    TYPE_EXTERNAL = 'external'

    TYPES = (
        TYPE_INTERNAL,
        TYPE_EXTERNAL
    )

    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUSES = (
        STATUS_PENDING,
        STATUS_ACCEPTED,
        STATUS_REJECTED
    )

    invite_type = db.Column(db.String(16), default=TYPE_EXTERNAL)
    status = db.Column(db.String(16), default=STATUS_PENDING)

    project_id = db.Column(
        db.Integer, db.ForeignKey('projects.id')
    )
    project = db.relationship(
        'Project',
        foreign_keys=project_id,
        backref=db.backref(
            'invites',
            lazy='dynamic',
            cascade="all, delete"
        )
    )

    email = db.Column(db.String(80), nullable=False)
    invite_link = db.Column(db.String(250))
    code = db.Column(db.String(80))
