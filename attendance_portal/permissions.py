from rest_framework import permissions
from .models import Session
from datetime import datetime


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_AUTHORIZATION_TOKEN' in request.META:
            auth_token = request.META['HTTP_AUTHORIZATION_TOKEN']
            user_type = 'student'

            session = Session.objects.filter(auth_token=auth_token, expires_at__gte=datetime.now()).first()

            return session and session.user_type == user_type
        else:
            return False


class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_AUTHORIZATION_TOKEN' in request.META:
            auth_token = request.META['HTTP_AUTHORIZATION_TOKEN']
            user_type = 'professor'

            session = Session.objects.filter(auth_token=auth_token, expires_at__gte=datetime.now()).first()

            return session and session.user_type == user_type
        else:
            return False
