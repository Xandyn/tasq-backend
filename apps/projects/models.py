# Stdlib imports

# Core Flask imports

# Third-party app imports
from sqlalchemy.dialects.postgresql import ARRAY

# Imports from your apps
from init.database import db, TimestampMixin, BaseModel


__all__ = (
    'Project',
)


class Project(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'projects'

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    owner = db.relationship(
        'User',
        foreign_keys=owner_id,
        backref=db.backref(
            'projects',
            lazy='dynamic',
            cascade="all, delete"
        )
    )

    collaborators = db.relationship(
        'User',
        secondary='collaborators',
        backref=db.backref(
            'invited_projects',
            lazy='dynamic',
            cascade="all, delete"
        ),
        lazy='dynamic'
    )

    name = db.Column(db.String(80), nullable=False)
    tasks_order = db.Column(ARRAY(db.Integer), default=[])
    is_shared = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)


collaborators = db.Table(
    'collaborators',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), nullable=False),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.PrimaryKeyConstraint('project_id', 'user_id')
)
