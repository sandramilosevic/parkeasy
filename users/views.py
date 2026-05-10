from django.shortcuts import render
from .models import User
from .serializers import UserSerialized, RegisterSerializer
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission
import logging

logger = logging.getLogger(__name__)


class UserPermission(BasePermission):
    """
    Custom permission for UserViewSet
    -Anyone can register (POST)
    -Only authenticated users can access other endpoints
    -Only admin can see list of all users
    -Only the user itself or admin can update or delete
    """

    def has_permission(self, request, view):
        # Anyone can register
        if request.method == 'POST':
            return True
        # Other actions require authentication
        if not request.user.is_authenticated:
            return False
        # Only admin can see list of all users
        if view.action == 'list':
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for authenticated users
        if request.method in SAFE_METHODS:
            return True
        # Only the user itself or admin can update or delete
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    Supports registation, profile view, update and delete
    """
    pagination_class = None
    queryset = User.objects.all()
    permission_classes = [UserPermission]

    def get_queryset(self):
        # Admin can see all users
        if self.request.user.is_staff:
            return User.objects.all()
        # Regular users can only see their own profile
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        # Use RegisterSerializer for registration (includes password)
        if self.action == 'create':
            return RegisterSerializer
        # Use UserSerialized for all other actions (excludes password)
        return UserSerialized

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f'New user registred {user.email}')