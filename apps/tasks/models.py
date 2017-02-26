# Stdlib imports

# Core Flask imports

# Third-party app imports

# Imports from your apps
from init.database import db, TimestampMixin, BaseModel


__all__ = (
    'Task',
)


class Task(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'tasks'

    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    creator = db.relationship(
        'User',
        foreign_keys=creator_id,
        backref=db.backref(
            'created_tasks',
            lazy='dynamic',
            cascade="all, delete"
        )
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id'),
        nullable=False
    )
    project = db.relationship(
        'Project',
        foreign_keys=project_id,
        backref=db.backref(
            'tasks',
            lazy='dynamic',
            cascade="all, delete"
        )
    )

    body = db.Column(db.String(80), nullable=False)
    note = db.Column(db.Text)
    notification_date = db.Column(db.DateTime(timezone=True))

    is_completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime(timezone=True))
    completed_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    completed_by_user = db.relationship(
        'User',
        foreign_keys=completed_by_user_id,
        backref=db.backref(
            'completed_tasks',
            lazy='dynamic',
            cascade="all, delete"
        )
    )

    assigned_to_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    assigned_to_user = db.relationship(
        'User',
        foreign_keys=assigned_to_user_id,
        backref=db.backref(
            'assigned_tasks',
            lazy='dynamic',
            cascade="all, delete"
        )
    )

    is_deleted = db.Column(db.Boolean, default=False)
