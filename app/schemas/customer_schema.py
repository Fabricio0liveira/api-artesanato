from marshmallow import Schema, fields, validate

class CustomerCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=False, allow_none=True, validate=validate.Length(max=100))
    phone_number = fields.Str(required=True, validate=validate.Length(min=8, max=20))

class CustomerResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    phone_number = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()