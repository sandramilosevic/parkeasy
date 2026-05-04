from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReservationPermission(BasePermission):
    """
    Custom permission for ReservationViewSet
    - Only authenticated users can access reservations
    - Only drivers can reate reservations
    - Only the user who made the reservation can update or delete it
    """

    def has_permission(self, request, view):
        # Only authenticated users can access reservations
        if not request.user.is_authenticated:
            return False
        # Only drivers can create reservations
        if request.method == 'POST':
            return request.user.user_type == 'driver'
        return True

    def has_object_permission(self, request, view, obj):
        # Allow read-onlu access for authenticated users
        if request.method in SAFE_METHODS:
            return True
        # Only the user who made the reservation can update or delete it
        return obj.reservation_user == request.user


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reservations
    Supports list, create, retrieve, update and delete operations
    """
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [ReservationPermission]

    def perform_create(self, serializer):
        # Automatically set reservation_user from JWT token
        serializer.save(reservation_user=self.request.user)

    def get_queryset(self):
        # Users can only see their own reservations
        return Reservation.objects.filter(reservation_user=self.request.user)
