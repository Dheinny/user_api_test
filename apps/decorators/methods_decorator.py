# -*- coding: utf-8 -*-

from mongoengine.errors import(
    DoesNotExist, FieldDoesNotExist
)

from flask_jwt_extended import get_jwt_identity

from apps.responses import(
    resp_exception, resp_resource_not_exists, resp_notallowed_user,
)

from apps.users.models import User
from apps.utils import get_user_by_user_name

class GetDecorator(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        try:
            return self.f(*args, **kwargs)
        
        except DoesNotExist as e:
            resource_info = kwargs.popitem()
            return resp_resource_not_exists("Resource", "Usuário", resource_info[1])

        except FieldDoesNotExist as e:
            return resp_expection("Users", description=e.__str__())

        except Exception as e:
            return resp_exception("Resource", description=e.__str__())

class AuthAdminDecorator(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        user = get_user_by_user_name(get_jwt_identity())
        if not isinstance(user, User):
            return user

        if user.is_admin():
            return self.f(*args, **kwargs)
        else:
            return resp_notallowed_user("Users")
