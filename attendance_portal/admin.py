# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(StudentCourse)
admin.site.register(Session)
admin.site.register(Lecture)
admin.site.register(Attendance)
admin.site.register(AttendanceToken)