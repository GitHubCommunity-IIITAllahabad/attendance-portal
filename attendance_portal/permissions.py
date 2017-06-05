from rest_framework import permissions
from .models import Session, Student, Professor
from datetime import datetime


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_AUTHORIZATION_TOKEN' in request.META:
            auth_token = request.META['HTTP_AUTHORIZATION_TOKEN']
            user_type = 'student'

            session = Session.objects.filter(auth_token=auth_token, expires_at__gte=datetime.now()).first()

            if session and session.user_type == user_type:
                user = Student.objects.get(pk=session.user_id)
                request.user = user
                return request
            else:
                return False
        else:
            return False


class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_AUTHORIZATION_TOKEN' in request.META:
            auth_token = request.META['HTTP_AUTHORIZATION_TOKEN']
            user_type = 'professor'

            session = Session.objects.filter(auth_token=auth_token, expires_at__gte=datetime.now()).first()

            if session and session.user_type == user_type:
                user = Professor.objects.get(pk=session.user_id)
                request.user = user
                return request
        else:
            return False
