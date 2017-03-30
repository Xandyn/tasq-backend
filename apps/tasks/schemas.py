# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import (
    Schema,
    fields,
)

# Imports from your apps


class TaskBaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    text = fields.String()
    note = fields.Raw(allow_none=True)

    notification_date = fields.DateTime(allow_none=True)
    completion_date = fields.DateTime(allow_none=True)

    is_completed = fields.Boolean(allow_none=True)
    completed_at = fields.DateTime(allow_none=True)

    is_deleted = fields.Boolean(load_only=True)


class TaskSchema(TaskBaseSchema):
    creator = fields.Nested('UserSchema', dump_only=True)
    project = fields.Nested('ProjectBaseSchema', dump_only=True)
    completed_by_user = fields.Nested('UserSchema', dump_only=True, allow_none=True)
    assigned_to_user = fields.Nested('UserSchema', dump_only=True, allow_none=True)


class TaskCreateSchema(Schema):
    text = fields.String(required=True)
    note = fields.Raw()

    notification_date = fields.DateTime(allow_none=True)
    completion_date = fields.DateTime(allow_none=True)

    project_id = fields.Integer(required=True)

    assigned_to_user_id = fields.Integer(allow_none=True)
