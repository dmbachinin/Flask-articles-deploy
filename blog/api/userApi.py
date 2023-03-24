from flask_combo_jsonapi import ResourceList, ResourceDetail

from blog.api.permissions.userPermissions import UserListPermissions, UserPatchPermissions
from blog.models import User
from blog.models.database import db
from blog.schemas import UserSchema


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
        'permission_get': [UserListPermissions],
    }


class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
        'short_format': [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        ],
        'permission_get': [UserListPermissions],
        'permission_patch': [UserPatchPermissions],
    }
