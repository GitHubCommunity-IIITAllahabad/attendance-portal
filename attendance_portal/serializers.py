from rest_framework import serializers
from .models import Student, Course


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('enrollment_no', 'first_name', 'last_name', 'email', 'current_semester', 'graduation_year')


class CourseSerializer(serializers.ModelSerializer):
    course_code = serializers.SerializerMethodField()

    def get_course_code(self, obj):
        return obj.course_code.upper()

    class Meta:
        model = Course
        fields = ('course_name', 'course_code')
