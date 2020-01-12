from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('location', views.LocationViewset, basename='location')

urlpatterns = [
    path('secrete_message/', views.SecretMessage.as_view())
]

urlpatterns += router.urls
