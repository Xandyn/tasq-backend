# Stdlib imports

# Core Flask imports
from flask_jwt import current_identity

# Third-party app imports
from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError
)

# Imports from your apps
from apps.users.schemas import UserSchema
from apps.projects.schemas import ProjectSchema


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    body = fields.String()
    note = fields.Raw()

    notification_date = fields.DateTime()
    completion_date = fields.DateTime()

    creator = fields.Nested(UserSchema, dump_only=True)
    project = fields.Nested(ProjectSchema, dump_only=True)

    is_completed = fields.Boolean()
    completed_by_user = fields.Nested(UserSchema, dump_only=True)
    completed_by_user_id = fields.Integer(load_only=True)

    assigned_to_user = fields.Nested(UserSchema, dump_only=True)
    assigned_to_user_id = fields.Integer(load_only=True)

    is_deleted = fields.Boolean(load_only=True)


class TaskCreateSchema(Schema):
    body = fields.String(required=True)
    note = fields.Raw()

    notification_date = fields.DateTime()
    completion_date = fields.DateTime()

    project_id = fields.Integer(required=True)

    assigned_to_user_id = fields.Integer()

    @validates('project_id')
    def validate_project_id(self, project_id):
        projects_ids = [x.id for x in current_identity.projects]
        projects_ids += [x.id for x in current_identity.invited_projects]
        if project_id not in projects_ids:
            raise ValidationError('Project doesnt exists.')
