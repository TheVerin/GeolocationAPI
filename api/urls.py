from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('get', views.LocationGet, basename='get')
router.register('create', views.LocationCreate, basename='create')
router.register('delete', views.LocationDelete, basename='delete')

urlpatterns = [
    path('secret_message/', views.SecretMessage.as_view()),
    path('location/', include(router.urls))
]
