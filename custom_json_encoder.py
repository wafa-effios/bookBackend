from flask.json import JSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        return super().default(obj)