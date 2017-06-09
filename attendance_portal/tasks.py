from background_task import background
from .models import *


@background(schedule=2)
def add_students_to_lecture(content):
    course = Course.objects.get(pk=content['course_id'])
    student_course_obj_list = StudentCourse.objects.filter(course=course, section=content['section'])

    for student_course_obj in student_course_obj_list:
        Attendance.objects.create(student_course=student_course_obj, lecture_id=content['lecture_id'])

    for token_info in content['tokens']:
        AttendanceToken.objects.create(token=token_info['token'], lecture_id=content['lecture_id'],
                                       token_issued=token_info['students'])

    course.total_lectures += 1
    course.save()
