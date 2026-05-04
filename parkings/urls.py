from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkingViewSet

router = DefaultRouter()
router.register('parkings', ParkingViewSet)

urlpatterns = [
    path('', include(router.urls))
]
