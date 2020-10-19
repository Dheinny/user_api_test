# -*- coding: utf-8 -*-

from mongoengine.errors import(
    DoesNotExist, FieldDoesNotExist
)

from apps.responses import(
    resp_exception, resp_resource_not_exists,
)

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
