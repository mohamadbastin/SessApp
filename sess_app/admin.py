from django.contrib import admin
from .models import *


# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_filter = ['department']
    list_display = ['title', 'teacher', 'group', 'vahed', 'unit']


admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserCourse)
admin.site.register(Note)
admin.site.register(ExamDate)
admin.site.register(Message)
admin.site.register(Operator)
admin.site.register(Report)
admin.site.register(PrivacyPolicy)
