from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)