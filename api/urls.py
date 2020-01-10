from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('location', views.LocationViewset, basename='location')


urlpatterns = router.urls
