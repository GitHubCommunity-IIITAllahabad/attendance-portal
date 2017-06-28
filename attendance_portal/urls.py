from django.conf.urls import url
from . import views

app_name = 'attendance_portal'
urlpatterns = [
    url(r'^students', views.StudentView.as_view(), name='students'),
    url(r'^login', views.UserLoginView.as_view(), name='login_user'),
    url(r'^student/course', views.StudentCourseView.as_view(), name='students_course'),
    url(r'^attendance-tokens', views.AttendanceTokenView.as_view(), name='tokens'),
    url(r'^attendance/student', views.StudentAttendanceView.as_view(), name='attendance_students'),
    url(r'faculty/course', views.ProfessorCourseView.as_view(), name='faculty_course'),
    url(r'^attendance/course', views.ProfessorAttendanceView.as_view(), name='attendance_course'),
    url(r'^logout', views.logout, name='logout_user'),
]
