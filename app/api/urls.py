from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('location', views.LocationViewset)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
