from django.conf.urls import url
from . import views

app_name = 'attendance_portal'
urlpatterns = [
    url(r'^students', views.StudentView.as_view()),
    url(r'^login', views.UserLoginView.as_view()),
    url(r'^student/course', views.StudentCourseView.as_view()),
    url(r'^attendance-tokens', views.AttendanceTokenView.as_view()),
    url(r'^attendance/student', views.StudentAttendanceView.as_view()),
    url(r'faculty/course', views.ProfessorCourseView.as_view()),
    url(r'^attendance/course', views.ProfessorAttendanceView.as_view()),
    url(r'^logout', views.logout)
]
