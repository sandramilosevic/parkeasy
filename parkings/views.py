from django.shortcuts import render
from .models import Parking
from .serializers import ParkingSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework import viewsets
import logging

logger = logging.getLogger(__name__)


class ParkingPermission(BasePermission):
    """
    Custom permission for ParkingViewSet
    -Anyone can read (GET)
    -Only authenticated users can create
    -Only API owner can update or delete

    """

    def has_permission(self, request, view):
        # Allow read-onlu access for unauthenticated users
        if request.method in SAFE_METHODS:
            return True
        # Only authenticated users can write
        if not request.user.is_authenticated:
            return False
        # Only owner can create parking
        if view.action == 'create':
            return request.user.user_type == 'owner'
        return True

    def has_object_permission(self, request, view, obj):
        # Allow read-onlu access for everyone
        if request.method in SAFE_METHODS:
            return True
        # Only owner can modify or delete
        return obj.owner == request.user


class ParkingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing parking spots.
    Supports list, create, retrieve, update and delete operations
    """
    serializer_class = ParkingSerializer
    permission_classes = [ParkingPermission]

    queryset = Parking.objects.none()

    filterset_fields = ['city', 'parking_type', 'distance']
    search_fields = ['title', 'city']
    ordering_fields = ['price_per_hour', 'price_per_day', 'price_per_month']

    def perform_create(self, serializer):
        # Automatically set owner from JWT token
        serializer.save(owner=self.request.user)
        logger.info(f'Parking created by {self.request.user}')

    def get_queryset(self):
        return Parking.objects.select_related('owner')
