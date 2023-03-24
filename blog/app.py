from flask import Flask
from flask_combo_jsonapi import Api
from flask_login import LoginManager
from flask_migrate import Migrate

from blog.admin import admin
from blog.configs import BaseConfig
from blog.models.database import db
from flask_wtf import CSRFProtect

login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
api = Api()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(BaseConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    # csrf.init_app(app)
    admin.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    register_blueprints(app)
    register_api(app)
    return app

def register_api(app: Flask):
    from blog.api.tagApi import TagList, TagDetail
    from blog.api.userApi import UserList, UserDetail
    from blog.api.authorApi import AuthorList, AuthorDetail
    from blog.api.articleApi import ArticleList, ArticleDetail

    from blog.api import create_ApiSpecPlugin, create_EventPlugin, create_PermissionPlugin


    api.plugins = [
        create_EventPlugin(),
        create_PermissionPlugin(),
        create_ApiSpecPlugin(app),
    ]
    api.init_app(app)

    api.route(TagList, 'tag_list', '/api/tags', tag="Tags")
    api.route(TagDetail, 'tag_detail', '/api/tags/<int:id>', tag="Tags")

    api.route(UserList, 'user_list', '/api/users', tag="User")
    api.route(UserDetail, 'user_detail', '/api/users/<int:id>', tag="User")

    api.route(AuthorList, 'author_list', '/api/authors', tag="Author")
    api.route(AuthorDetail, 'author_detail', '/api/authors/<int:id>', tag="Author")

    api.route(ArticleList, 'article_list', '/api/articles', tag="Article")
    api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>', tag="Article")

def register_blueprints(app: Flask):
    from blog.user.views import userBlueprint
    from blog.auth.views import authBlueprint
    from blog.author.views import authorBlueprint
    from blog.articles.views import articleBlueprint

    app.register_blueprint(userBlueprint)
    app.register_blueprint(authorBlueprint)
    app.register_blueprint(articleBlueprint)
    app.register_blueprint(authBlueprint)
