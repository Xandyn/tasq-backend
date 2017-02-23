# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import (
    Schema,
    fields
)

# Imports from your apps
from apps.users.models import Invite
from apps.users.schemas import UserSchema, InviteSchema


class ProjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    owner = fields.Nested(UserSchema, dump_only=True)
    owner_id = fields.Integer()

    collaborators = fields.Nested(UserSchema, many=True)
    # invites = fields.Nested(InviteSchema, many=True)

    tasks_order = fields.List(fields.Integer(), default=[])

    is_shared = fields.Boolean()
    is_deleted = fields.Boolean()

    # pending_collaborators = fields.Method('get_pending_collaborators', dump_only=True)
    #
    # def get_pending_collaborators(self, obj):
    #     invites = Invite.query.filter(
    #         Invite.project_id == obj.id,
    #         Invite.status == Invite.STATUS_PENDING
    #     ).all()
    #
    #     return [
    #         {'email': invite.email, 'type': invite.invite_type}
    #         for invite in invites
    #     ]
