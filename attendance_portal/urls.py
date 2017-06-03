from django.conf.urls import url
from . import views

app_name = 'attendance_portal'
urlpatterns = [
    url(r'^students/', views.StudentView.as_view())
]