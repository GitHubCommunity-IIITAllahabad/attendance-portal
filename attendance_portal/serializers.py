from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('enrollment_no', 'first_name', 'last_name', 'email', 'current_semester', 'graduation_year')


class ManyStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('enrollment_no', 'first_name', 'last_name')
