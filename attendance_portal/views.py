# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Student, StudentCourse, Course, Attendance, Session, Professor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta, datetime
from .ldaplogin import authenticate_user


class UserLoginView(APIView):
    def post(self, request):
        user_type = request.data['userType']

        if 'HTTP_AUTHORIZATION_TOKEN' in request.META and Session.objects.filter(
                auth_token=request.META['HTTP_AUTHORIZATION_TOKEN'],
                expires_at__gte=datetime.now(),
                user_type=user_type).exists():
            return Response({"message": "User already logged in"}, status=status.HTTP_200_OK)
        else:
            username = request.data['userName'].lower()
            password = request.data['password']
            # NOTE The following code is only meant for development purposes until ldap login function is tested against
            # the university ldap server.
            # When the function is battle-tested, uncomment the following line and comment out the if statement
            # is_user = authenticate_user(username, password, user_type)
            if user_type == 'professor':
                is_user = Professor.objects.filter(professor_id=username).exists()
            else:
                is_user = Student.objects.filter(enrollment_no=username).exists()

            if is_user:
                auth_token = get_random_string(length=64,
                                               allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                if user_type == 'professor':
                    user_id = Professor.objects.get(professor_id=username).id
                else:
                    user_id = Student.objects.get(enrollment_no=username).id

                Session.objects.create(auth_token=auth_token, user_id=user_id, user_type=user_type,
                                       expires_at=timezone.now() + timedelta(hours=5))
                payload = {
                    "authToken": auth_token,
                    "userId": username,
                    "userType": user_type
                }

                return Response(payload, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "Given Credentials are wrong"}, status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    def put(self, request):
        roll_no = request.data['rollNo'].lower()
        first_name = request.data['firstName']
        last_name = request.data['lastName']
        email = request.data['email']
        current_semester = request.data['currentSemester']
        graduation_year = request.data['graduationYear']

        student = Student.objects.filter(enrollment_no=roll_no).first()

        if student:
            if student.is_active is True:
                student.enrollment_no = roll_no
                student.first_name = first_name
                student.last_name = last_name
                student.email = email
                student.current_semester = current_semester
                student.graduation_year = graduation_year
                student.save()

                return Response({"message": "Student info updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The student does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            Student.objects.create(
                enrollment_no=roll_no,
                first_name=first_name,
                last_name=last_name,
                email=email,
                current_semester=current_semester,
                graduation_year=graduation_year,
                is_active=True
            )

            return Response({"message": "Student Created"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        roll_no = request.GET['rollNo']
        student = Student.objects.filter(enrollment_no=roll_no, is_active=True).first()

        if student:
            payload = StudentSerializer(instance=student).data
            return Response(payload, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)
