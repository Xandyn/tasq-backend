# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import (
    Schema,
    fields
)

# Imports from your apps


class FileSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    key = fields.String()
