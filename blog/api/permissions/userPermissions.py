from combojsonapi.permission import PermissionMixin, PermissionUser, PermissionForGet, PermissionForPatch
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user

from blog.models import User


class UserListPermissions(PermissionMixin):
    ALL_AVAILABLE_FIELD = {
        "id",
        "first_name",
        "last_name",
        "email",
        "is_staff",
    }

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        if not current_user.is_authenticated:
            raise AccessDenied('No access')

        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELD, 10)

        return self.permission_for_get


class UserPatchPermissions(PermissionMixin):

    PATCH_AVAILABLE_FIELDS = (
        "first_name",
        "last_name",
    )

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data=None, obj=None, user_permission: PermissionUser = None, **kwargs) -> dict:
        permission_for_patch = user_permission.permission_for_patch_data(model=User)
        return {
            key: val
            for key, val in data.items()
        }