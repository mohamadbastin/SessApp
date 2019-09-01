from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(UserCourse)
admin.site.register(Note)
admin.site.register(ExamDate)
admin.site.register(Message)
admin.site.register(Operator)


