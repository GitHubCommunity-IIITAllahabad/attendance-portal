# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Student, StudentCourse, Course, Attendance
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer


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
