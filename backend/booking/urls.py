from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (BookingAPI, BusAPI, BusViewSet, CityViewSet, RouteAPI,
                    RouteViewSet, SeatViewSet)

router = DefaultRouter()

router.register(r"city", CityViewSet, basename="city")
router.register(r"route", RouteViewSet, basename="route")
router.register(r"bus", BusViewSet, basename="bus")
router.register(r"seat", SeatViewSet, basename="seat")

urlpatterns = router.urls

urlpatterns += [
    path("book/", BookingAPI.as_view(), name="booking"),
    path("buses/", BusAPI.as_view(), name="bus"),
    path("search/", RouteAPI.as_view(), name="search"),
]
