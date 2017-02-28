# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import (
    Schema,
    fields,
)

# Imports from your apps


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    text = fields.String()
    note = fields.Raw()

    notification_date = fields.DateTime()
    completion_date = fields.DateTime()

    creator_id = fields.Integer(dump_only=True)
    project_id = fields.Integer(dump_only=True)

    is_completed = fields.Boolean()
    completed_by_user_id = fields.Integer()
    completed_at = fields.DateTime()

    assigned_to_user_id = fields.Integer()

    is_deleted = fields.Boolean(load_only=True)


class TaskCreateSchema(Schema):
    text = fields.String(required=True)
    note = fields.Raw()

    notification_date = fields.DateTime()
    completion_date = fields.DateTime()

    project_id = fields.Integer(required=True)

    assigned_to_user_id = fields.Integer()
