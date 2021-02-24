from rest_framework import permissions
from users.models import User


class TeacherPermission(permissions.BasePermission):
    """
    permission to check if the user is a teacher.
    """
    message = 'Must be a Teacher.'

    def has_permission(self, request, view):
        if request.user.role == User.TEACHER:
            return True
        return False


class StudentPermission(permissions.BasePermission):
    """
    permission to check if the user is a student.
    """
    message = 'Must be a Student.'

    def has_permission(self, request, view):
        if request.user.role == User.STUDENT:
            return True
        return False
