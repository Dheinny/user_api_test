# -*- coding: utf-8

# Import API and Resource
from flask_restful import Api, Resource

from apps.users.resources import SignUp, UserResource, UserPassword 
from apps.users.resources_admin import AdminUserList

class Index(Resource):

    def get(self):
        return {'hello': 'world by apps'}

api = Api()

def configure_api(app):
    api.add_resource(Index, "/")
    api.add_resource(SignUp, "/users")
    api.add_resource(AdminUserList, "/admin/users")
    api.add_resource(UserResource, "/users/<string:username>")
    api.add_resource(UserPassword, "/users/<string:username>/password")
    api.init_app(app)
