from background_task import background
from .models import Course, StudentCourse, Attendance
from datetime import datetime


@background(schedule=2)
def add_students_to_lecture(content):
    course = Course.objects.get(pk=content['course_id'])
    student_course_obj_list = StudentCourse.objects.filter(course=course, section=content['section'])
    lecture_date_string = content['date'] + ' ' + content['time']
    lecture_datetime = datetime.strptime(lecture_date_string, '%d-%m-%Y %I:%M%p')
    flag = True

    for student_course_obj in student_course_obj_list:
        if not Attendance.objects.filter(student_course=student_course_obj, lecture_date=lecture_datetime,
                                         no_of_lectures=content['no_of_lectures'],
                                         lecture_type=content['lecture_type']).exists():
            Attendance.objects.create(student_course=student_course_obj, lecture_date=lecture_datetime,
                                      no_of_lectures=content['no_of_lectures'], lecture_type=content['lecture_type'])
        else:
            flag = False

    if flag:
        course.total_lectures += 1
        course.save()
