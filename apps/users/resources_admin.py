# -*- coding: utf-8 -*-

from flask import request

from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from mongoengine.errors import FieldDoesNotExist
from marshmallow import EXCLUDE

from apps.decorators.methods_decorator import AuthAdminDecorator
from apps.responses import resp_ok, resp_exception, resp_does_not_exist_resources
from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED

from apps.users.models import User
from apps.users.schemas import UserSchema

class AdminUserList(Resource):
    @jwt_required
    @AuthAdminDecorator
    def get(self):
        schema = UserSchema(many=True)

        args = request.args
        page_id = int(args["page"]) if args.get("page") else 1
        page_size = int(args["page_size"]) if args.get("page_size") and args.get("page_size") < 1 \
                else 10

        try:

            users = User.objects()
            count = users.count()
            if count == 0:
                return resp_does_not_exist_resources("User", "usuário")

            if count <= ((page_id-1)*page_size):
                page_id = ceil(count/page_size)
            users = users.paginate(page_id, page_size)

        except FieldDoesNotExist as e:
            return resp_exception("Users", description=e.__str__()+"field")

        except Exception as e:
            return resp_exception("Users", description=e.__str__())

        extra = {
            "page": users.page, "pages": users.pages, "total": users.total, 
            "params": {"page_size":page_size}
        }

        result = schema.dump(users.items)
        return resp_ok(
                "Users", MSG_RESOURCE_FETCHED_PAGINATED.format("Usuários"), result, **extra)

