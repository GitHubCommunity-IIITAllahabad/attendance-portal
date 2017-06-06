from django.conf.urls import url
from . import views

app_name = 'attendance_portal'
urlpatterns = [
    url(r'^students/', views.StudentView.as_view()),
    url(r'^login', views.UserLoginView.as_view()),
    url(r'^student-course', views.StudentCourseView.as_view()),
    url(r'^attendance$', views.AttendanceView.as_view())
]
