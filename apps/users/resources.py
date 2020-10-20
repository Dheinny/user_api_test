# -*- coding: utf-8 -*-

from flask import request

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from bcrypt import gensalt, hashpw, checkpw
from mongoengine.errors import NotUniqueError, ValidationError
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from apps.responses import(
    resp_already_exists,
    resp_resource_not_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok,
    resp_ok_no_content
)

from apps.users.models import User
from apps.users.schemas import UserRegistrationSchema, UserSchema, UserUpdateSchema
from apps.utils import check_password_in_signup, save_model, get_user_by_user_name

from apps.messages import (
    MSG_CHECK_PASSWORD_FAILED, MSG_NO_DATA, MSG_INVALID_DATA, MSG_RESOURCE_CREATED,
    MSG_RESOURCE_FETCHED, MSG_RESOURCE_UPDATED, MSG_PASSWORD_CHANGED,
)

from apps.decorators.methods_decorator import AuthenticationDecorator


class SignUp(Resource):
    def post(self, *args, **kwargs):
        req_data = request.get_json() or None
        data, erros, result = None, None, None
        password, confirm_password = None, None
        schema = UserRegistrationSchema()

        if req_data is None:
            return resp_data_invalid("Users", [], msg=MSG_NO_DATA)

        password = req_data.get("password")
        confirm_password = req_data.pop("confirm_password")

        if not check_password_in_signup(password, confirm_password):
            errors = {"password": MSG_CHECK_PASSWORD_FAILED}
            return resp_data_invalid("Users", errors)

        try:
            data= schema.load(req_data)

        except MarshmallowValidationError as e:
            return resp_data_invalid("Users", e.messages)

        hashed = hashpw(password.encode("utf-8"), gensalt(12))

        data["password"] = hashed
        data["email"] = data["email"].lower()
        model = User(**data)

        save_result = save_model(model, "Users", "Usuário")
        if not isinstance(save_result, User):
            return save_result

        schema = UserSchema()
        result = schema.dump(model)

        return resp_ok(
            "Users", MSG_RESOURCE_CREATED.format("Usuário"), data=result
        )


class UserResource(Resource):
    @jwt_required
    @AuthenticationDecorator
    def put(self, username):
        schema = UserSchema()
        up_schema = UserUpdateSchema()
        req_data = request.get_json() or None

        user = get_user_by_user_name(username)
        if not isinstance(user, User):
            return user

        try:
            user_up = up_schema.load(req_data, unknown=EXCLUDE)
        except MarshmallowValidationError as e:
            return resp_data_invalid("Users", e.messages)

        if user_up.get("user_name") and user_up.get("user_name") != username:
            return resp_data_invalid("Users", {"user_name": user_up.get("user_name")}, "Nao pode alterar o nome de usuário")

        try:
            for k, v in user_up.items():
                if k == "address":
                    for k_addr, v_addr in v.items():
                        user["address"][k_addr] = v_addr
                else:
                    user[k] = v

        except Exception as e:
            return resp_exception("Users-Aqui", description=e.__str__())


        save_result = save_model(user, "Users", "Usuário")
        if not isinstance(save_result, User):
            return save_result
        
        result = schema.dump(save_result)
        
        return resp_ok(
            "Users", MSG_RESOURCE_UPDATED.format("Usuário", username), data=result
        )


    @staticmethod
    @jwt_required
    @AuthenticationDecorator
    def get(username):
        schema = UserSchema()
        user = get_user_by_user_name(username)
        if not isinstance(user, User):
            return user

        result = schema.dump(user)

        return resp_ok(
            "Users", MSG_RESOURCE_FETCHED.format("Usuário", username), result)

    @staticmethod
    @jwt_required
    @AuthenticationDecorator
    def delete(username):
        schema = UserSchema()
        user = get_user_by_user_name(username)
        if not isinstance(user, User):
            return user

        user.delete()        

        return resp_ok_no_content()

class UserPassword(Resource):
    @jwt_required
    @AuthenticationDecorator
    def put(self, username):
        
        req_data = request.get_json() or None

        user = get_user_by_user_name(username)
        if not isinstance(user, User):
            return user
        
        current_password = req_data.get("current_password")
        new_password = req_data.get("new_password")
        confirm_password = req_data.pop("confirm_password")

        if not checkpw(current_password.encode("utf-8"), user["password"].encode("utf-8")):
            return resp_data_invalid("Users", "Senha atual não confere com a senha cadastrada")

        if not check_password_in_signup(new_password, confirm_password):
            errors = {"password": MSG_CHECK_PASSWORD_FAILED}
            return resp_data_invalid("Users", errors)

        new_pass_hashed = hashpw(new_password.encode("utf-8"), gensalt(12)).decode("utf-8")
        user["password"] = new_pass_hashed

        save_result = save_model(user, "Users", "Usuário")
        if not isinstance(save_result, User):
            return save_result
        
        return resp_ok("User", MSG_PASSWORD_CHANGED, data={"user_name": username})


