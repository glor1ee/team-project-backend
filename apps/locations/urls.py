from rest_framework.routers import DefaultRouter

from apps.locations.views import CityViewSet

app_name = "locations"

router = DefaultRouter()
router.register("cities", CityViewSet, basename="city")

urlpatterns = router.urls
