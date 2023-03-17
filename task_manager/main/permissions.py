from rest_framework import permissions


class TaskBase(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            if request.user.is_staff:
                return True

        if request.method == "POST":
            if request.user.role == "manager" or request.user.is_staff:
                return True

        if request.method in (permissions.SAFE_METHODS + ("PUT", "PATCH")):
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        if request.user == getattr(obj, "author"):
            allowed_fields = [
                "executor",
                "description",
                "deadline",
                "priority",
                "tags",
                "state",
            ]
            if all(field in allowed_fields for field in request.data):
                return True

        if request.user == getattr(obj, "executor"):
            allowed_fields = ["tags", "state"]
            if all(field in allowed_fields for field in request.data):
                return True


class UserBase(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            if request.user.is_staff:
                return True

        if request.method in (permissions.SAFE_METHODS + ("PUT", "PATCH")):
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user == obj and request.user.is_staff:
            allowed_fields = [
                "username",
                "name",
                "surname",
                "email",
                "role",
                "avatar_picture",
                "delete_avatar",
            ]
            if all(field in allowed_fields for field in request.data):
                return True

        if request.user.is_staff:
            allowed_fields = ["role"]
            if all(field in allowed_fields for field in request.data):
                return True

        if request.user == obj:
            allowed_fields = [
                "username",
                "name",
                "surname",
                "email",
                "avatar_picture",
                "delete_avatar",
            ]
            if all(field in allowed_fields for field in request.data):
                return True


class TagBase(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        if request.method == "POST":
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True
