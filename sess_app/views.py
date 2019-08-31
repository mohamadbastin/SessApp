from django.shortcuts import render
from random import randint

from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView
# Create your views here.
from rest_framework.response import Response

from sms.models import Message, Operator
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
import requests
import urllib.request
import time
import json
from bs4 import BeautifulSoup


# Create your views here.


class SignupView(CreateAPIView):
    serializer_class = UserGetOrCreate

    allowed_methods = ['POST', ]

    def post(self, request, *args, **kwargs):
        the_serializer = self.serializer_class(data=request.data)

        if not the_serializer.is_valid():
            return Response({'errors': the_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = request.data.get('phone', None)
        # department = request.data.get('department', None)

        try:
            userr = User.objects.get(username=phone_number)
            profile = Profile.objects.get(user=userr)
            return Response({"status": "has account"})

        except (Profile.DoesNotExist, User.DoesNotExist):
            user = User.objects.create(username=phone_number)
            profile = Profile.objects.create(user=user, phone=phone_number)
            # if department != None:
            #     department = Department.objects.get(pk=department)
            #     profile.department = department
            profile.save()

        password = randint(1000, 9999)

        user.set_password(password)
        user.save()

        message = Message(message="کلمه عبور یکبار مصرف کرسی شما: %d" % password, to=phone_number)
        operator = Operator.objects.first()
        operator.send_message(message)
        return Response({"password": 'sent'})


class LoginView(CreateAPIView):
    serializer_class = UserGetOrCreate

    allowed_methods = ['POST', ]

    def post(self, request, *args, **kwargs):
        the_serializer = self.serializer_class(data=request.data)

        if not the_serializer.is_valid():
            return Response({'errors': the_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = request.data.get('phone', None)
        # department = request.data.get('department', None)

        try:
            userr = User.objects.get(username=phone_number)
            profile = Profile.objects.get(user=userr)
            user = profile.user
            # return Response({"status": "has account"})
        except User.DoesNotExist:
            # user = User.objects.create(username=phone_number)
            # profile = Profile.objects.create(user=user, phone=phone_number)
            # # if department != None:
            # #     department = Department.objects.get(pk=department)
            # #     profile.department = department
            # profile.save()
            return Response({"status": "no account"})

        password = randint(1000, 9999)

        user.set_password(password)
        user.save()

        message = Message(message="کلمه عبور یکبار مصرف کرسی شما: %d" % password, to=phone_number)
        operator = Operator.objects.first()
        operator.send_message(message)
        return Response({"password": 'sent'})


class UpdateProfileView(CreateAPIView):
    serializer_class = ProfileSerializer1
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        dep = Department.objects.get(pk=self.request.data.get('department', None))
        user.department = dep
        user.name = self.request.data.get('name', None)
        user.picture = self.request.data.get('picture', None)
        # user.department = self.request.data.get('department', None)
        user.save()

        return Response({"status": "done"})


class DeleteProfileView(CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        user.delete()
        usr.delete()

        return Response({"status": "done"})


# class DepartmentUpdateView(CreateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         usr = self.request.user
#         user = Profile.objects.get(user=usr)
#
#         dep = request.data.get('department', None)
#
#         user.department = dep
#         user.save()


class DepartmentView(ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        dp_id = self.kwargs.get('department_id')

        if dp_id == '__all__':
            return Department.objects.all()
        # print(self.kwargs)
        # print (dp_id)
        return Department.objects.filter(pk=dp_id)


class CourseView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cs_id = self.kwargs.get('course_id')
        if cs_id == '__all__':
            return Course.objects.all()
        return Course.objects.filter(pk=cs_id)


class DepartmentCourseView(ListAPIView):
    serializer_class = CourseSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dp_id = self.kwargs.get('dp_id')
        dp = Department.objects.get(pk=dp_id)
        return Course.objects.filter(department=dp)


class NoteCreateView(CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            cr = Course.objects.get(pk=kwargs.get('cr_id', None), )
            uc = UserCourse.objects.get(user_profile=user, course=cr)
            a = Note.objects.create(text=request.data.get('text', ' '), user_course=uc,
                                    date=request.data.get('date', ' '))

            return Response({"status": "done", "pk": a.pk})
        except UserCourse.DoesNotExist:
            return Response({"status": "cr not correct"})


class UserCourseListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseSerializer

    def get_queryset(self):
        cr_id = self.kwargs.get('cr_id')

        usr = self.request.user
        user = Profile.objects.get(user=usr)

        if cr_id == '__all__':
            return UserCourse.objects.filter(user_profile=user)
        # print(self.kwargs)
        # print (dp_id)
        cr = Course.objects.get(pk=cr_id)
        return UserCourse.objects.filter(course=cr, user_profile=user)


class CreateDatabaseView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateDatabaseSerializer

    def post(self, request, *args, **kwargs):
        pwd = request.data.get('pwd', None)
        if pwd != 'amirmohamad':
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        else:

            f = open('13981.txt')
            a = json.load(f)
            for dep in a:
                try:
                    last_dp = Department.objects.get(dep_id=dep['id'])
                    last_dp.title = dep['title']
                    for cs in dep['courses']:
                        try:
                            last_cs = Course.objects.get(cs_id=cs['ident'])
                            last_cs.title, last_cs.group, last_cs.teacher, last_cs.gender, last_cs.final_time, last_cs.time_room = \
                                cs['title'], cs['group'], cs['teacher'], cs['gender'], cs['final_date'], cs['time_room']

                            last_cs.department = last_dp
                            last_cs.save()
                            last_dp.save()
                        except Course.DoesNotExist:
                            Course.objects.create(title=cs['title'], group=cs['group'], teacher=cs['teacher'],
                                                  gender=cs['gender'], final_time=cs['final_date'],
                                                  time_room=cs['time_room'], department=last_dp, cs_id=cs['ident'])
                except Department.DoesNotExist:
                    last_dp = Department.objects.create(title=dep['title'], dep_id=dep['id'])
                    for cs in dep['courses']:
                        Course.objects.create(title=cs['title'], group=cs['group'], teacher=cs['teacher'],
                                              gender=cs['gender'], final_time=cs['final_date'],
                                              time_room=cs['time_room'], department=last_dp, cs_id=cs['ident'])

            return Response({"status": "done"})


class CleanDatabaseView(CreateAPIView):
    serializer_class = CreateDatabaseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pwd = request.data.get('pwd', None)
        if pwd != 'amirmohamad':
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            for i in Department.objects.all():
                # print(i.title)
                if i.courses.all():
                    continue
                else:
                    i.delete()
            return Response({"status": "done"})


class ProfileView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # pr_id = self.kwargs.get('')

        # if pr_id == '__all__':
        #     return Profile.objects.all()
        # elif pr_id == None:
        #     usr = self.request.user
        #     user = Profile.objects.filter(user=usr)
        #     return user
        # else:
        #     return Profile.objects.filter(pk=pr_id)

        usr = self.request.user
        user = Profile.objects.filter(user=usr)

        return user


class NoteUpdateView(CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            nt_id = self.kwargs.get('nt_id')
            a = Note.objects.get(pk=nt_id)
            a.text = self.request.data.get('text', ' ')
            a.date = self.request.data.get('date', ' ')
            a.save()
            return Response({"status": "done"})
        except Note.DoesNotExist:
            return Response({"status": "note not correct"})


class NoteDeleteView(CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            nt_id = self.kwargs.get('nt_id')
            a = Note.objects.get(pk=nt_id)
            a.delete()
            return Response({"status": "done"})
        except Note.DoesNotExist:
            return Response({"status": "note not correct"})


class UserCourseCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseSerializer

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        cs_id = self.kwargs.get('cs_id', None)

        try:
            cs = Course.objects.get(pk=cs_id)
            a = UserCourse.objects.create(user_profile=user, course=cs)
            return Response({"status": "done", "id": a.pk})

        except Course.DoesNotExist:
            return Response({"status": "course id not correct"})


class UserCourseDeleteView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseSerializer

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        cs_id = self.kwargs.get('cs_id', None)

        try:
            cs = Course.objects.get(pk=cs_id)
            a = UserCourse.objects.get(user_profile=user, course=cs)
            a.delete()
            return Response({"status": "done"})

        except Course.DoesNotExist:
            return Response({"status": "course id not correct"})


class ExamDateCreateView(CreateAPIView):
    serializer_class = ExamDateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            cr = Course.objects.get(pk=kwargs.get('cr_id', None), )
            uc = UserCourse.objects.get(user_profile=user, course=cr)
            ExamDate.objects.create(title=self.request.data.get('title', None),
                                    date=self.request.data.get('date', None),
                                    user_course=uc,
                                    grade=self.request.data.get('grade', None))
            return Response({"status": "done"})
        except UserCourse.DoesNotExist:
            return Response({"status": "cr not correct"})


class ExamDateUpdateView(CreateAPIView):
    serializer_class = ExamDateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            uc = ExamDate.objects.get(pk=self.kwargs.get('ex_id', None))
            uc.title = self.request.data.get('title', uc.title)
            uc.date = self.request.data.get('date', uc.date)
            uc.grade = self.request.data.get('grade', uc.grade)
            uc.save()

            return Response({"status": "done"})

        except UserCourse.DoesNotExist:
            return Response({"status": "ex not correct"})


class ExamDateDeleteView(CreateAPIView):
    serializer_class = ExamDateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            uc = ExamDate.objects.get(pk=self.kwargs.get('ex_id', None))
            uc.delete()
            return Response({"status": "done"})
        except UserCourse.DoesNotExist:
            return Response({"status": "ex not correct"})
