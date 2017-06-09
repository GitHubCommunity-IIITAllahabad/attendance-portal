# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Student, StudentCourse, Course, AttendanceToken, Session, Professor, Attendance
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import StudentSerializer, CourseSerializer, AttendanceSerializer
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta, datetime
from .permissions import IsProfessor, IsStudent
from .tasks import add_students_to_lecture
from .helper_functions import get_tokens, authenticate_user


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

                return Response(payload, status=status.HTTP_200_OK)
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
            course_id_list = student.studentcourse_set.all().values_list('course_id', flat=True)
            course_obj_list = Course.objects.filter(pk__in=course_id_list)
            courses = CourseSerializer(instance=course_obj_list, many=True).data
            student_info = StudentSerializer(instance=student).data
            payload = {
                "studentInfo": student_info,
                "coursesTaken": courses
            }

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


class AttendanceTokenView(APIView):
    permission_classes = (IsProfessor,)

    def post(self, request):
        course = Course.objects.filter(course_code=request.data['course'].lower()).first()

        if course:
            content = {
                "course_id": course.id,
                "section": request.data['section'].upper(),
                "date": request.data['date'],
                "time": request.data['time'].upper(),
                "no_of_lectures": request.data['noOfLectures'],
                "lecture_type": request.data['lectureType']
            }
            add_students_to_lecture(content)
            payload = get_tokens(int(request.data['totalStudents']), int(request.data['noOfTokens']))
            datetime_obj = datetime.strptime(request.data['date'] + ' ' + request.data['time'].upper(),
                                             '%d-%m-%Y %I:%M%p')

            for token_info in payload:
                AttendanceToken.objects.create(token=token_info['token'], course=course, lecture_date=datetime_obj,
                                               token_issued=token_info['students'])

            return Response(payload, status=status.HTTP_200_OK)
        else:
            return Response({"message": "The entered course does not exist", "course": course['course']},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        token = request.data['token']
        course_code = request.data['course']
        increase_by = request.data['increaseBy']
        course = Course.objects.filter(course_code=course_code.lower()).first()

        if course:
            attendance_token_obj = AttendanceToken.objects.filter(course=course, token=token).first()

            if attendance_token_obj:
                attendance_token_obj.token_issued += int(increase_by)
                attendance_token_obj.save()

                return Response({"message": "Token capacity increased"}, status=status.HTTP_200_OK)

        return Response({"message": "Check the values entered"}, status=status.HTTP_400_BAD_REQUEST)


class StudentAttendanceView(APIView):
    permission_classes = (IsStudent,)

    def put(self, request):
        student = request.user
        course_code = request.data['course']
        course = Course.objects.filter(course_code=course_code.lower()).first()

        if course:
            token = request.data['attendanceToken']
            attendance_token_obj = AttendanceToken.objects.filter(token=token, course=course).first()

            if attendance_token_obj:
                if attendance_token_obj.token_accepted < attendance_token_obj.token_issued:
                    attendance_token_obj.token_accepted += 1
                    attendance_token_obj.save()

                    student_course = StudentCourse.objects.get(student=student, course=course)
                    student_course.lectures_attended += 1
                    student_course.save()

                    attendance = Attendance.objects.get(student_course=student_course,
                                                        lecture_date=attendance_token_obj.lecture_date)
                    attendance.is_present = True
                    attendance.save()

                    return Response(
                        {"message": "Attendance marked of " + student.enrollment_no + " for the course " + course_code},
                        status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"message": "The token is no longer valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"message": "The entered token is wrong"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "The entered course is wrong"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        student = request.user
        course_code = request.GET['course']
        course = Course.objects.filter(course_code=course_code.lower()).first()

        if course:
            student_course = StudentCourse.objects.filter(student=student, course=course).first()

            if student_course:
                attendance_record = Attendance.objects.filter(student_course=student_course)
                attendance_data = AttendanceSerializer(instance=attendance_record, many=True).data
                lectures_attended = student_course.lectures_attended
                total_lectures = course.total_lectures
                attendance_percentage = (lectures_attended * 100) / float(total_lectures)
                payload = {
                    "totalLectures": str(total_lectures),
                    "lecturesAttended": str(lectures_attended),
                    "percentage": str(attendance_percentage)[:5] + "%",
                    "attendance": attendance_data
                }

                return Response(payload, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The student does not take this course"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "The entered course is wrong"}, status=status.HTTP_404_NOT_FOUND)


class ProfessorCourseView(APIView):
    permission_classes = (IsProfessor,)

    def post(self, request):
        professor = request.user
        course_code = request.data['course']
        course = Course.objects.filter(course_code=course_code.lower()).first()

        if course:
            professor.courses.add(course)

            return Response({"message": "Course " + course_code + " added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Entered course is wrong"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        professor = request.user
        courses = professor.courses.all()
        payload = CourseSerializer(instance=courses, many=True).data

        return Response(payload, status=status.HTTP_200_OK)

    def delete(self, request):
        professor = request.user
        course = Course.objects.filter(course_code=request.data['course'].lower()).first()

        if course:
            professor.courses.remove(course)

            return Response({"message": "Course " + request.data['course'] + " removed"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Entered course is wrong"}, status=status.HTTP_404_NOT_FOUND)


class ProfessorAttendanceView(APIView):
    permission_classes = (IsProfessor,)

    def get(self, request):
        course_code = request.GET['course'].lower()
        month = request.GET['month']
        section = request.GET['section'].upper()
        course = Course.objects.filter(course_code=course_code).first()

        if course:
            student_course_obj_list = StudentCourse.objects.filter(course=course, section=section)
            payload = []

            for student_course in student_course_obj_list:
                student = student_course.student
                enrollment_no = student.enrollment_no
                name = student.first_name + ' ' + student.last_name
                attendance = Attendance.objects.filter(student_course=student_course, lecture_date__month=month)
                attendance_data = AttendanceSerializer(instance=attendance, many=True).data
                content = {
                    "enrollmentNo": enrollment_no,
                    "name": name,
                    "attendanceData": attendance_data
                }
                payload.append(content)

            return Response(payload, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Entered course is wrong"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def logout(request):
    if 'HTTP_AUTHORIZATION_TOKEN' in request.META:
        auth_token = request.META['HTTP_AUTHORIZATION_TOKEN']
        session = Session.objects.filter(auth_token=auth_token).first()

        if session:
            session.expires_at = datetime.now()
            session.save()

            return Response({"message": "You are logged out"}, status=status.HTTP_200_OK)

    return Response({"message": "There was something wrong"}, status=status.HTTP_400_BAD_REQUEST)
