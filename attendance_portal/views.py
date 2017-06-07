# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Student, StudentCourse, Course, AttendanceToken, Session, Professor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer, ManyStudentsSerializer
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta, datetime
from .permissions import IsProfessor, IsStudent
from .tasks import add_students_to_lecture
from .helper_functions import get_tokens
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
            # When the function is battle-tested, uncomment the following line and comment out statement after that
            # is_user = authenticate_user(username, password, user_type)
            is_user = True
            first_name = request.data['firstName']
            last_name = request.data['lastName']
            email = request.data['email']

            if is_user:
                auth_token = get_random_string(length=64,
                                               allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                if user_type == 'professor':
                    user = Professor.objects.filter(professor_id=username).first()
                    if user:
                        user_id = user.id
                    else:
                        new_user = Professor.objects.create(professor_id=username, first_name=first_name,
                                                            last_name=last_name, email=email)
                        user_id = new_user.id
                else:
                    user = Student.objects.filter(enrollment_no=username).first()
                    if user:
                        user_id = user.id
                    else:
                        new_user = Student.objects.create(enrollment_no=username, first_name=first_name,
                                                          last_name=last_name, email=email, is_active=True)
                        user_id = new_user.id

                Session.objects.create(auth_token=auth_token, user_id=user_id, user_type=user_type,
                                       expires_at=timezone.now() + timedelta(hours=4))
                payload = {
                    "authToken": auth_token,
                    "userId": username,
                    "userType": user_type
                }

                return Response(payload, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "Given Credentials are wrong"}, status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    permission_classes = (IsStudent,)

    def put(self, request):
        student = request.user

        if student.is_active is True:
            student.first_name = request.data['firstName']
            student.last_name = request.data['lastName']
            student.email = request.data['email']
            student.current_semester = request.data['currentSemester']
            student.graduation_year = request.data['graduationYear']
            student.save()

            return Response({"message": "Student info updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "The student does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        roll_no = request.user.enrollment_no
        student = Student.objects.filter(enrollment_no=roll_no, is_active=True).first()

        if student:
            payload = StudentSerializer(instance=student).data

            return Response(payload, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)


class StudentCourseView(APIView):
    permission_classes = (IsStudent,)

    def put(self, request):
        semester = request.data['semester']
        course_data = request.data['courseData']
        student = request.user
        student.current_semester = semester
        student.save()

        for course in course_data:
            a_course = Course.objects.filter(course_code=course['course'].lower()).first()

            if a_course:
                student_course = StudentCourse.objects.filter(student=student, course=a_course,
                                                              semester=semester).first()

                if student_course:
                    student_course.section = course['section']
                    student_course.save()
                else:
                    StudentCourse.objects.create(student=student, course=a_course, semester=semester,
                                                 section=course['section'])
            else:
                return Response({"message": "The entered course does not exist", "course": course['course']},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Courses updated"}, status=status.HTTP_200_OK)


class AttendanceView(APIView):
    permission_classes = (IsProfessor,)

    def post(self, request):
        course = Course.objects.filter(course_code=request.data['course'].lower()).first()

        if course:
            content = {
                "course_id": course.id,
                "semester": request.data['semester'],
                "section": request.data['section'].upper(),
                "date": request.data['date'],
                "time": request.data['time'].upper(),
                "no_of_lectures": request.data['noOfLectures'],
                "lecture_type": request.data['lectureType']
            }
            add_students_to_lecture(content)
            payload = get_tokens(int(request.data['totalStudents']), int(request.data['noOfTokens']))

            for token_info in payload:
                AttendanceToken.objects.create(token=token_info['token'], course=course,
                                               token_issued=token_info['students'])

            return Response(payload, status=status.HTTP_200_OK)
        else:
            return Response({"message": "The entered course does not exist", "course": course['course']},
                            status=status.HTTP_404_NOT_FOUND)
