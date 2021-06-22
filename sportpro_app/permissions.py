from rest_framework import permissions


class CoachAccessPermission(permissions.BasePermission):
    message = 'Editing players not allowed'

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Coach").exists()

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class EditorAccessPermission(permissions.BasePermission):
    message = 'Editing news not allowed'

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Editor").exists()

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class AdminAccessPermission(permissions.BasePermission):
    message = 'Editing federation not allowed'

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admin").exists()

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class JudgeAccessPermission(permissions.BasePermission):
    message = 'Editing federation not allowed'

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Judge").exists()

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id