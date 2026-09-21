from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=6, error="Senha precisa ter no mínimo 6 caracteres.")
    )

class UserResponseSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    created_at = fields.DateTime()

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserProfileSchema(Schema):
    id = fields.Int()
    email = fields.Email()