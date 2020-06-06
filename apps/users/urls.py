from rest_framework.routers import SimpleRouter, Route

from .views import UserViewSet


class UserRouter(SimpleRouter):

    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/profile/$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]


user_router = UserRouter()
user_router.register('', UserViewSet, basename='users')
urlpatterns = user_router.get_urls()
