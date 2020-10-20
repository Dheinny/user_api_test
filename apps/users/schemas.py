# -*- coding: utf-8 -*-

from marshmallow import Schema
from marshmallow.fields import Email, Str, Boolean, Nested, DateTime, Date

from apps.messages import (MSG_FIELD_REQUIRED)
class AddressSchema(Schema):
    zip_code = Str()
    street = Str()
    number = Str()
    complement = Str()
    neighborhood = Str()
    city = Str()
    state = Str()
    country = Str()


class UserRegistrationSchema(Schema):
    full_name = Str(required=True, error_messages={"required": MSG_FIELD_REQUIRED})
    user_name = Str(required=True, error_messages={"required": MSG_FIELD_REQUIRED})
    email = Email(required=True, error_messages={"required": MSG_FIELD_REQUIRED})
    date_of_born = Date()
    address = Nested(AddressSchema)
    phone = Str()
    admin = Boolean()
    password = Str(required=True, error_messages={"required": MSG_FIELD_REQUIRED})


class UserSchema(Schema):
    full_name = Str(required=True, error_messages={"required": MSG_FIELD_REQUIRED})
    user_name = Str(required=True, error_messages={"required": MSG_FIELD_REQUIRED})
    email = Email(required=True, error_messages={"required": MSG_FIELD_REQUIRED})
    date_of_born = Date()
    address = Nested(AddressSchema)
    phone = Str()
    admin = Boolean()
    active = Boolean()


class UserUpdateSchema(Schema):
    full_name = Str()
    user_name = Str()
    email = Email()
    date_of_born = Date()
    address = Nested(AddressSchema)
    phone = Str()
    admin = Boolean()
    active = Boolean()



