from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('enrollment_no', 'first_name', 'last_name', 'email', 'current_semester', 'graduation_year')


class CourseSerializer(serializers.ModelSerializer):
    course_code = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    def get_course_code(self, obj):
        return obj.course_code.upper()

    def get_course_name(self, obj):
        return obj.course_name.title()

    class Meta:
        model = Course
        fields = ('course_name', 'course_code')


class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    no_of_lectures = serializers.SerializerMethodField()
    lecture_type = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.lecture.lecture_date.strftime("%d-%m-%Y")

    def get_time(self, obj):
        return obj.lecture.lecture_date.strftime("%I:%M%p")

    def get_no_of_lectures(self, obj):
        return obj.lecture.no_of_lectures

    def get_lecture_type(self, obj):
        return obj.lecture.lecture_type

    class Meta:
        model = Attendance
        fields = ('date', 'time', 'no_of_lectures', 'lecture_type', 'is_present')


class AttendanceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceToken
        fields = ('token', 'token_issued')
