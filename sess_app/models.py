import json

import requests
from django.db import models

# Create your models here.
from django.contrib.auth.admin import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=1000, )
    picture = models.CharField(null=True, blank=True, max_length=1000000000000000)

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
    vahed = models.CharField(max_length=10)
    unit = models.CharField(max_length=1000)

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
    date = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.text[:10] + ' / ' + str(self.user_course)


class ExamDate(models.Model):
    title = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, related_name="exam_dates", on_delete=models.CASCADE)
    grade = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return str(self.title) + ' / ' + str(self.user_course)


class Message(models.Model):
    to = models.CharField(max_length=15)
    token = models.CharField(max_length=100000)
    token2 = models.CharField(max_length=1000000, null=True, blank=True)
    token3 = models.CharField(max_length=1000000, null=True, blank=True)

    block_code = models.IntegerField(blank=True, null=True)

    last_try = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.to) + " : " + str(self.token)


class Operator(models.Model):
    name = models.CharField(max_length=255)
    template = models.CharField(max_length=255)

    # username = models.CharField(max_length=255, verbose_name=_("Username"), help_text=_("User name given by operator"
    # password = models.CharField(max_length=255, verbose_name=_("Password"), help_text=_("Password given by operator"))

    # sender = models.CharField(max_length=15, verbose_name=_("Sender Phone Number"),
    #                           help_text=_("The operator phone number"))

    # retry_gap_time = models.IntegerField(verbose_name=_("Retry Gap Time"),
    #                                      help_text=_("Time in minutes before you can try to send a message again"))

    api_endpoint = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def send_message(self, message):

        # api = furl(self.api_endpoint)
        #
        # api.args['uname'] = self.username
        # api.args['pass'] = self.password
        # api.args['from'] = self.sender
        # api.args['msg'] = message.message
        # api.args['to'] = message.to

        # check for retry gap
        # now = timezone.now()
        # if message.last_try is None:
        #     message.last_try = now - timezone.timedelta(minutes=self.retry_gap_time * 2)

        # if now - message.last_try >= timezone.timedelta(minutes=self.retry_gap_time):
        # eligible to retry

        # message.last_try = now
        data = {"receptor": message.to, "template": self.template, "token": message.token, "token2": message.token2,
                "token3": message.token3}
        r = requests.post(self.api_endpoint, data=data)

        try:
            # print(r)
            # print(1)
            # print(json.loads(r.text))
            # print(2)
            block_code = json.loads(r.text)[1]["entries"][0]["messageid"]
            message.block_code = block_code
        except:
            err = json.loads(r.text)
            return {'status': 'OK', 'msg': err[1]}

        # tdo: fix bug on retry gap if fails
        message.save()

        return {'status': 'OK', 'msg': "Message Sent"}

    # else:
    #     return {'status': 'NOK', 'msg': _("try again later")}
    # not eligible to retry


class Report(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=100000)

    def __str__(self):
        return str(self.user) + str(self.text[:20])


class PrivacyPolicy(models.Model):
    pp = models.CharField(max_length=100000)
    tos = models.CharField(max_length=100000)
