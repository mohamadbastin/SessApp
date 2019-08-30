from django.db import models

# Create your models here.
from django.contrib.auth.admin import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=1000,)
    picture = models.ImageField(null=True, blank=True)

    courses = models.ManyToManyField('Course', through='UserCourse')

    def __str__(self):
        return str(self.user.username)


class Department(models.Model):
    title = models.CharField(max_length=100)
    dep_id = models.CharField(max_length=100)

    # course = models.ForeignKey('Course', on_delete=models.CASCADE)
    @property
    def get_courses(self):
        return self.courses.all()

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, related_name="courses", on_delete=models.CASCADE)
    teacher = models.CharField(max_length=200)
    group = models.CharField(max_length=10)
    time_room = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    final_time = models.CharField(max_length=100)
    cs_id = models.CharField(max_length=100)

    profiles = models.ManyToManyField(Profile, through='UserCourse')

    # def get_user_course(self):
    #     uc = self.user_course.all()
    #     l = []
    #     for i in uc:
    #         l.append(i.user_profile)
    #
    #     return l

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user_profile = models.ForeignKey(Profile, related_name='user_course', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='user_course', on_delete=models.CASCADE)

    # note = models.ForeignKey

    def get_notes(self):
        return self.notes.all()

    def get_exam_date(self):
        return self.exam_dates.all()

    def __str__(self):
        return str(self.user_profile) + ' --> ' + str(self.course)


class Note(models.Model):
    text = models.CharField(max_length=2000)
    user_course = models.ForeignKey(UserCourse, related_name="notes", on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10] + ' / ' + str(self.user_course)


class ExamDate(models.Model):
    title = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, related_name="exam_dates", on_delete=models.CASCADE)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
