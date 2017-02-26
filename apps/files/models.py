# Stdlib imports

# Core Flask imports

# Third-party app imports

# Imports from your apps
from init.database import db, TimestampMixin, BaseModel

__all__ = (
    'File',
)


class File(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'files'

    name = db.Column(db.String(250))
    key = db.Column(db.String(250))
