from rest_framework import permissions


class IsAdminModeratorAuthorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if view.action == 'partial_update' or view.action == 'destroy':
            return (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
            )
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_admin or request.user.is_superuser
        return False


class IsAdminOrAnon(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or not request.user.is_anonymous
            and (request.user.is_admin or request.user.is_superuser)
        )
