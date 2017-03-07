# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import (
    Schema,
    fields,
)

# Imports from your apps


class BaseTaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    text = fields.String()
    note = fields.Raw()

    notification_date = fields.DateTime()
    completion_date = fields.DateTime()

    is_completed = fields.Boolean()
    completed_at = fields.DateTime()

    is_deleted = fields.Boolean(load_only=True)


class TaskSchema(BaseTaskSchema):
    creator_id = fields.Integer(dump_only=True)
    project_id = fields.Integer(dump_only=True)
    completed_by_user_id = fields.Integer()
    assigned_to_user_id = fields.Integer()


class TaskSchemaAll(BaseTaskSchema):
    creator = fields.Integer(attribute='creator_id')
    project = fields.Integer(attribute='project_id')
    completed_by_user = fields.Integer(attribute='completed_by_user_id')
    assigned_to_user = fields.Integer(attribute='assigned_to_user_id')


class TaskCreateSchema(Schema):
    text = fields.String(required=True)
    note = fields.Raw()

    notification_date = fields.DateTime()
    completion_date = fields.DateTime()

    project_id = fields.Integer(required=True)

    assigned_to_user_id = fields.Integer()
