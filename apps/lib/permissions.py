from rest_framework import permissions
from .loggers import AppLogger


class IsAdminOrReadOnly(permissions.BasePermission):
    """
        Allows read-only access for any request, but restricts write operations
        (POST, PUT, PATCH, DELETE) to staff users only.

        Security:
            Logs unauthorized write attempts to AppLogger.log_security.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_staff = bool(request.user and request.user.is_staff)
        if not is_staff:
            AppLogger.log_security(f"Unauthorized Staff Attempt: {request.method}", user=request.user,
                                   path=request.path)
        return is_staff


class IsAdmin(permissions.BasePermission):
    """
        Strict permission that only allows access to staff users for all HTTP methods.
        Used for administrative endpoints.
    """

    def has_permission(self, request, view):
        is_staff = bool(request.user and request.user.is_staff)
        if not is_staff:
            AppLogger.log_security(f"Unauthorized Staff Attempt: {request.method}", user=request.user,
                                   path=request.path)
        return is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        Object-level permission that allows anyone to view an object (GET),
        but only allows the creator (owner) to modify or delete it.

        Security:
            Logs attempts by users trying to manipulate data they don't own.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = obj.user == request.user
        if not is_owner:
            AppLogger.log_security(
                msg=f"OWNERSHIP VIOLATION | Tried to {request.method} post_id={obj.id}",
                user=request.user,
                path=request.path
            )
        return is_owner
