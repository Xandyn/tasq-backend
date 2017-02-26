# Stdlib imports
import uuid

# Core Flask imports

# Third-party app imports
from flask_jwt import current_identity
from werkzeug.security import generate_password_hash
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    post_load,
    ValidationError
)

# Imports from your apps
from apps.files.schemas import FileSchema
from apps.users.models import User


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    email = fields.Email()
    avatar = fields.Nested(FileSchema)

    @validates('email')
    def validate_email(self, email):
        try:
            user = User.query.filter(User.email == email.lower()).one()
            if user.id == current_identity.id:
                user = None
        except NoResultFound:
            user = None

        if user:
            raise ValidationError('This email already taken.')


class UserRegistrationSchema(Schema):
    name = fields.String()
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @post_load
    def hash_password(self, in_data):
        in_data['password'] = generate_password_hash(in_data['password'])
        return in_data

    @post_load
    def lower_email(self, in_data):
        in_data['email'] = in_data['email'].lower().strip()
        return in_data

    @validates('email')
    def validate_email(self, email):
        try:
            user = User.query.filter(User.email == email.lower()).one()
        except NoResultFound:
            user = None

        if user:
            raise ValidationError('This email already taken.')

    @validates_schema
    def validate_passwords(self, obj):
        if len(obj['password']) < 6:
            raise ValidationError(
                'Your password must be at least 6 characters.',
                ['password', ]
            )


class UserNameUpdateSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class InviteSchema(Schema):
    id = fields.Integer(dump_only=True)
    code = fields.String()
    invite_link = fields.String()
    invite_type = fields.String()
    status = fields.String()
    email = fields.Email()
    project_id = fields.Integer()

    @post_load
    def generate_code(self, in_data):
        if 'code' not in in_data:
            in_data['code'] = str(uuid.uuid3(uuid.uuid1(), in_data['email']))
        return in_data
