# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports
from flask import current_app, jsonify, request
from flask.views import MethodView

# Third-party app imports
from flask_jwt import jwt_required, current_identity
from sqlalchemy.orm.exc import NoResultFound

# Imports from your apps
from init.database import db
from init.utils import parse_json_to_object, generate_jwt_token, send_email

from apps.users.models import User, Invite
from apps.users.schemas import (
    UserSchema,
    UserRegistrationSchema,
    UserNameUpdateSchema,
    InviteSchema
)


__all__ = (
    'ProfileView',
    'InviteView'
)


class ProfileView(MethodView):
    @jwt_required()
    def get(self):
        data = UserSchema().dump(current_identity).data
        return jsonify(data)

    def post(self):
        json_data = request.get_json()
        result = UserRegistrationSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        user = User()
        parse_json_to_object(user, result.data)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'token': generate_jwt_token(str(user.id))
        })

    @jwt_required()
    def put(self):
        json_data = request.get_json()
        user = User.query.get(current_identity.id)
        result = UserNameUpdateSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        parse_json_to_object(user, result.data)
        db.session.add(user)
        db.session.commit()

        data = UserSchema().dump(user).data
        return jsonify(data)


class InviteView(MethodView):
    @jwt_required()
    def post(self):
        json_data = request.get_json()

        invite_type = Invite.TYPE_EXTERNAL
        try:
            user = User.query.filter(
                User.email == json_data['email']).one()
        except NoResultFound:
            user = None

        if user:
            invite_type = Invite.TYPE_INTERNAL
        json_data['invite_type'] = invite_type

        result = InviteSchema().load(json_data)

        if result.errors:
            return jsonify(result.errors), 403

        invite = Invite()
        parse_json_to_object(invite, result.data)

        db.session.add(invite)
        db.session.flush()

        invite_link = "{0}{1}/".format(
            current_app.config['INVITE_REG_LINK'],
            result.data['code'])
        send_email(
            'test.html',
            {
                "link": invite_link,
                "user_id": current_identity.id
            },
            u"Invite test",
            [result.data['email']]
        )
        invite.invite_link = invite_link

        db.session.add(invite)
        db.session.commit()

        data = InviteSchema().dump(invite).data
        return jsonify(data)

    @jwt_required()
    def delete(self):
        return jsonify()
