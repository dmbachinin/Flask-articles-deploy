from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
from combojsonapi.spec import ApiSpecPlugin


def create_ApiSpecPlugin(app):
    api_spec_plugin = ApiSpecPlugin(
        app=app,
        tags={
            'Tags': 'Tags API',
            'User': 'User API',
            'Author': 'Author API',
            'Article': 'Article API',
        }
    )
    return api_spec_plugin


def create_EventPlugin():
    return EventPlugin()

def create_PermissionPlugin():
    return PermissionPlugin()