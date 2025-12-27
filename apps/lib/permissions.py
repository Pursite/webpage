from rest_framework import permissions
from .loggers import AppLogger


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_staff = bool(request.user and request.user.is_staff)
        if not is_staff:
            AppLogger.log_security(f"Unauthorized Staff Attempt: {request.method}", user=request.user,
                                   path=request.path)
        return is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
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