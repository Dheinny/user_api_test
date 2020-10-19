#-*- coding: utf-8 -*-

from flask import request

from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from bcrypt import checkpw

from apps.users.models import User
from apps.users.schemas import UserSchema
from apps.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.responses import (
    resp_ok, resp_data_invalid, resp_notallowed_user, resp_exception
)

from apps.auth.schemas import LoginSchema

class AuthResource(Resource):
    def post(self, *args, **kwargs):
        """
        Rota para login na API
        """
        req_data = request.get_json() or None
        user = None
        login_schema = LoginSchema()
        user_schema = UserSchema(exclude=["address"])
        
        if req_data is None:
            return resp_data_invalid("Users", [], msg=MSG_NO_DATA)

        try:
            data = login_schema.load(req_data)

        except MarshmallowValidationError as e:
            return resp_data_invalid("Users", desc=e.__str__())

        try:
            user = User.objects.get(user_name=data["user_name"])
        except Exception as e:
            return resp_exception("Users", description=e.__str__())

        if not isinstance(user, User):
            return user

        if checkpw(data.get("password").encode("utf-8"), user.password.encode("utf-8")):
            extras = {
                "token": create_access_token(identity=user.user_name),
                "refresh": create_refresh_token(identity=user.user_name)
            }

            result = user_schema.dump(user)

            return resp_ok(
                "Auth", MSG_TOKEN_CREATED, data=result, **extras
            )

        return resp_notallowed_user("Auth")
