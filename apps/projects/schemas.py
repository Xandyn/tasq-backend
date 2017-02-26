# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import (
    Schema,
    fields
)

# Imports from your apps
from apps.users.models import Invite
from apps.users.schemas import UserSchema


class ProjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()

    owner = fields.Nested(UserSchema, dump_only=True)

    tasks_order = fields.List(fields.Integer(), default=[])

    is_shared = fields.Boolean()
    is_deleted = fields.Boolean(load_only=True)

    collaborators = fields.Nested(UserSchema, many=True, dump_only=True)
    pending_collaborators = fields.Method(
        'get_pending_collaborators', dump_only=True
    )

    def get_pending_collaborators(self, obj):
        invites = Invite.query.filter(
            Invite.project_id == obj.id,
            Invite.status == Invite.STATUS_PENDING
        ).all()

        return [
            {'email': invite.email, 'type': invite.invite_type}
            for invite in invites
        ]


class ProjectCreateSchema(Schema):
    name = fields.String(required=True)
    is_shared = fields.Boolean()


class CollaboratorDeleteSchema(Schema):
    project_id = fields.Integer(load_only=True, required=True)
    collaborator_id = fields.Integer(load_only=True, required=True)
