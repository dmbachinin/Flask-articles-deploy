from flask import redirect
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import MethodNotAllowed

from blog import models
from blog.models.database import db


class BaseAdminView(ModelView):

   def is_accessible(self):
       return current_user.is_authenticated and current_user.is_staff

   def inaccessible_callback(self, name, **kwargs):
       raise MethodNotAllowed('Недостаточно прав доступа для данного ресурса')


class BaseAdminIndexView(AdminIndexView):
    @expose()
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect("/")
        return super(BaseAdminIndexView, self).index()


class TagAdminView(BaseAdminView):
    column_searchable_list = ('name',)


class ArticleAdminView(BaseAdminView):
    can_export = True
    export_types = ('xlsx', 'csv')

class UserAdminView(BaseAdminView):
    column_exclude_list = ('password', )
    can_create = False
    can_delete = False
    column_editable_list = ('first_name', 'last_name', 'is_staff')


admin = Admin(name="Blog Admin Panel", template_mode="bootstrap4", index_view=BaseAdminIndexView())

admin.add_view(TagAdminView(models.Tag, db.session, category="Models"))
admin.add_view(ArticleAdminView(models.Article, db.session, category="Models"))
admin.add_view(BaseAdminView(models.Author, db.session, category="Models"))
admin.add_view(UserAdminView(models.User, db.session, category="Models"))

