from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'attendance_portal'
urlpatterns = [
    url(r'^api/students', views.StudentView.as_view(), name='students'),
    url(r'^api/login', views.UserLoginView.as_view(), name='login_user'),
    url(r'^api/student/course', views.StudentCourseView.as_view(), name='students_course'),
    url(r'^api/attendance-tokens', views.AttendanceTokenView.as_view(), name='tokens'),
    url(r'^api/attendance/student', views.StudentAttendanceView.as_view(), name='attendance_students'),
    url(r'api/faculty/course', views.ProfessorCourseView.as_view(), name='faculty_course'),
    url(r'^api/attendance/course', views.ProfessorAttendanceView.as_view(), name='attendance_course'),
    url(r'^api/logout', views.logout, name='logout_user'),
    url(r'^$', TemplateView.as_view(template_name="attendance_portal/login-page.html")),
    url(r'^student$', TemplateView.as_view(template_name="attendance_portal/index.html")),
    url(r'^professor$', TemplateView.as_view(template_name="attendance_portal/index_professor.html"))
]
