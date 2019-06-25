from rest_framework import permissions
from django.contrib import admin

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return ((request.user.is_staff) or str(obj.host)==str(request.user))

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.methodin permissions.SAFE_METHODS:
            return True
        return str(obj.host)==str(request.user)