from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

schema_view = get_schema_view(
    openapi.Info(
        title='Geolocation',
        default_version='v1'
    )
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/v1/', include('api.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('token/', obtain_jwt_token, name='token_obtain_pair'),
    path('token/refresh/', refresh_jwt_token, name='token_refresh')
]
