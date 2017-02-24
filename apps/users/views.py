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
        """Invite user to project

        ``Example request``:

        .. sourcecode:: http

            POST /invites HTTP/1.1
            Accept: application/json
            Content-Type: application/json
            JWTAuthorization: JWT <jwt_token>

            {
                "email": "mail@example.com",
                "project_id": 1
            }


        ``Example response``:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": "380eca36-4a8d-30f5-969e-ff8363c592f8",
                "email": "mail@example.com",
                "id": 1,
                "invite_link": "http://localhost:3000/invite/380eca36-4a8d-30f5-969e-ff8363c592f8/",
                "invite_type": "external",
                "project_id": 1,
                "status": "pending"
            }
        """
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

        try:
            invite = Invite.query.filter(
                Invite.email == result.data['email'],
                Invite.project_id == int(result.data['project_id']),
                Invite.status != Invite.STATUS_REJECTED
            ).one()
            return jsonify({
                'error': 'This user already invited.'
            }), 403
        except NoResultFound:
            invite = Invite()

        parse_json_to_object(invite, result.data)

        db.session.add(invite)
        db.session.flush()

        invite_link = "{0}{1}/".format(
            current_app.config['INVITE_REG_LINK'],
            result.data['code']
        )
        send_email(
            'invite.html',
            {
                "link": invite_link,
                "email": current_identity.email,
                "username": current_identity.name,
                "project": invite.project.name
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
        """Reject invite

        ``Example request``:

        .. sourcecode:: http

            POST /invites HTTP/1.1
            Accept: application/json
            Content-Type: application/json
            JWTAuthorization: JWT <jwt_token>

            {
                "email": "mail@example.com",
                "project_id": 1,
                "code": "380eca36-4a8d-30f5-969e-ff8363c592f8"
            }


        ``Example response``:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {}
        """
        json_data = request.get_json()

        try:
            invite = Invite.query.filter(
                Invite.email == json_data['email'],
                Invite.project_id == int(json_data['project_id']),
                Invite.status == Invite.STATUS_PENDING,
                Invite.code == json_data['code']
            ).one()
        except NoResultFound:
            return jsonify({
                'error': 'Invite doesnt exists.'
            }), 403

        invite.status = Invite.STATUS_REJECTED

        db.session.add(invite)
        db.session.commit()

        return jsonify({})