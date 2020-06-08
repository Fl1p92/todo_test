"""todo_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
]

api_patterns = [
    path('api/v1/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/todos/', include('apps.tasks.urls')),
]

urlpatterns += api_patterns


if settings.GENERATE_AUTO_DOCS:
    schema_view = get_schema_view(
        openapi.Info('ToDo Test', 'v1', 'ToDo Test description'),
        patterns=api_patterns,
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
