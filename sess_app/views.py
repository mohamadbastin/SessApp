from django.shortcuts import render
from random import randint

from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView
# Create your views here.
from rest_framework.response import Response

# from sms.models import Message, Operator
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
            print('n: ', profile.name)
            if profile.name != '':
                h = {"status": 400, "text": "شماره شما قبلا ثبت شده.ورود کنید."}
                return Response({"status": 400, "text": "شماره شما قبلا ثبت شده.\nورود کنید."}, headers=h)
            else:
                raise Exception(User.DoesNotExist)

        except:
            try:
                user = User.objects.get(username=phone_number)
            except User.DoesNotExist:
                user = User.objects.create(username=phone_number)
            profile = Profile.objects.create(user=user, phone=phone_number)
            # if department != None:
            #     department = Department.objects.get(pk=department)
            #     profile.department = department
            profile.save()

        password = randint(1000, 9999)

        user.set_password(password)
        user.save()

        message = Message(token=password, to=phone_number)

        operator = Operator.objects.get(name="sahar")
        operator.send_message(message)
        h = {"text": "password sent", "status": 200}
        return Response({"text": "password sent", "status": 200}, headers=h)


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
            h = {"status": 404, "text": "شماره شما ثبت نشده.ثبت نام کنید."}
            return Response({"status": 404, "text": "شماره شما ثبت نشده.\nثبت نام کنید."}, headers=h)

        password = randint(1000, 9999)

        user.set_password(password)
        user.save()

        message = Message(token=password, to=phone_number)

        operator = Operator.objects.get(name="sahar")
        operator.send_message(message)
        h = {"text": 'password sent', "status": 200}
        return Response({"text": 'password sent', "status": 200}, headers=h)


class UpdateProfileView(CreateAPIView):
    serializer_class = ProfileSerializer1
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        dep = Department.objects.get(pk=self.request.data.get('department', user.department))
        user.department = dep
        user.name = self.request.data.get('name', user.name)
        user.picture = self.request.data.get('picture', user.picture)
        # user.department = self.request.data.get('department', None)
        user.save()

        h = {"status": 200}
        return Response({"status": 200}, headers=h)


class DeleteProfileView(CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        user.delete()
        usr.delete()
        h = {"status": 200}
        return Response({"status": 200}, headers={"status": 200})


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

            h = {"status": 200, "pk": a.pk}
            return Response({"status": 200, "pk": a.pk}, headers=h)
        except UserCourse.DoesNotExist:
            h = {"text": "cr not correct", "status": 404}
            return Response({"text": "cr not correct", "status": 404},
                            headers={"text": "cr not correct", "status": 404})


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
    # permission_classes = [IsAuthenticated]
    serializer_class = CreateDatabaseSerializer

    def post(self, request, *args, **kwargs):
        pwd = request.data.get('pwd', None)
        if pwd != 'amirmohamad':
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        else:

            f = open('sess_app/13981.txt')
            a = json.load(f)
            for dep in a:
                try:
                    last_dp = Department.objects.get(dep_id=dep['id'])
                    last_dp.title = dep['title']
                    for cs in dep['courses']:
                        try:
                            last_cs = Course.objects.get(cs_id=cs['ident'])
                            last_cs.title, last_cs.group, last_cs.teacher, last_cs.gender, last_cs.final_time, \
                            last_cs.time_room, last_cs.vahed, last_cs.unit = \
                                cs['title'], cs['group'], cs['teacher'], cs['gender'], cs['final_date'], cs[
                                    'time_room'], cs['vahed'], cs['unit']

                            last_cs.department = last_dp
                            last_cs.save()
                            last_dp.save()
                        except Course.DoesNotExist:
                            Course.objects.create(title=cs['title'], group=cs['group'], teacher=cs['teacher'],
                                                  gender=cs['gender'], final_time=cs['final_date'],
                                                  time_room=cs['time_room'], department=last_dp, cs_id=cs['ident'],
                                                  vahed=cs['vahed'], unit=cs['unit'])
                except Department.DoesNotExist:
                    last_dp = Department.objects.create(title=dep['title'], dep_id=dep['id'])
                    for cs in dep['courses']:
                        Course.objects.create(title=cs['title'], group=cs['group'], teacher=cs['teacher'],
                                              gender=cs['gender'], final_time=cs['final_date'],
                                              time_room=cs['time_room'], department=last_dp, cs_id=cs['ident'],
                                              vahed=cs['vahed'], unit=cs['unit'])

            return Response({"status": 200}, headers={"status": 200})


class CleanDatabaseView(CreateAPIView):
    serializer_class = CreateDatabaseSerializer

    # permission_classes = [IsAuthenticated]

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
            return Response({"status": 200}, headers={"status": 200})


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
            a.text = self.request.data.get('text', a.text)
            a.date = self.request.data.get('date', a.date)
            a.save()
            return Response({"status": 200}, headers={"status": 200})
        except Note.DoesNotExist:
            return Response({"text": "nt not correct", "status": 404},
                            headers={"text": "nt not correct", "status": 404})


class NoteDeleteView(CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            nt_id = self.kwargs.get('nt_id')
            a = Note.objects.get(pk=nt_id)
            a.delete()
            return Response({"status": 200}, headers={"status": 200})
        except Note.DoesNotExist:
            return Response({"text": "nt not correct", "status": 404},
                            headers={"text": "nt not correct", "status": 404})


class UserCourseCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseSerializer

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        cs_id = self.kwargs.get('cs_id', None)

        try:
            cs = Course.objects.get(pk=cs_id)
            b = UserCourse.objects.filter(user_profile=user, course=cs)
            if b:
                return Response({"text": "already enrolled", "status": 400},
                                headers={"text": "already enrolled", "status": 400})
            a = UserCourse.objects.create(user_profile=user, course=cs)
            return Response({"status": 200, "id": a.pk}, headers={"status": 200, "id": a.pk})

        except Course.DoesNotExist:
            return Response({"text": "cr not correct", "status": 404},
                            headers={"text": "cr not correct", "status": 404})


class UserCourseDeleteView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseSerializer

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        cs_id = self.kwargs.get('cs_id', None)

        try:
            cs = Course.objects.get(pk=cs_id)
            a = UserCourse.objects.filter(user_profile=user, course=cs)

            for i in a:
                a.delete()
            return Response({"status": 200}, headers={"status": 200})

        except Course.DoesNotExist:
            return Response({"text": "cr not correct", "status": 404},
                            headers={"text": "cr not correct", "status": 404})


class ExamDateCreateView(CreateAPIView):
    serializer_class = ExamDateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            cr = Course.objects.get(pk=kwargs.get('cr_id', None), )
            uc = UserCourse.objects.get(user_profile=user, course=cr)
            ex = ExamDate.objects.create(title=self.request.data.get('title', None),
                                         date=self.request.data.get('date', None),
                                         user_course=uc,
                                         grade=self.request.data.get('grade', None))
            return Response({"status": 200, "pk": ex.pk}, headers={"status": 200, "pk": ex.pk})
        except UserCourse.DoesNotExist:
            return Response({"text": "cr not correct", "status": 404},
                            headers={"text": "cr not correct", "status": 404})


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

            return Response({"status": 200}, headers={"status": 200})

        except ExamDate.DoesNotExist:
            return Response({"text": "ex not correct", "status": 404},
                            headers={"text": "ex not correct", "status": 404})


class ExamDateDeleteView(CreateAPIView):
    serializer_class = ExamDateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)
        try:
            uc = ExamDate.objects.get(pk=self.kwargs.get('ex_id', None))
            uc.delete()
            return Response({"status": 200}, headers={"status": 200})
        except ExamDate.DoesNotExist:
            return Response({"text": "ex not correct", "status": 404}, {"text": "ex not correct", "status": 404})


class ChangeNumberFirst(CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        new_pn = self.request.data.get('phone', None)
        if new_pn:
            try:
                User.objects.get(username=new_pn)
                h = {"status": 400, "text": "شماره شما قبلا ثبت شده.ورود کنید."}
                return Response({"status": 400, "text": "شماره شما قبلا ثبت شده.\nورود کنید."}, headers=h)
            except User.DoesNotExist:
                password = randint(1000, 9999)

                usr.first_name = password
                usr.save()

                message = Message(token=password, to=new_pn)

                operator = Operator.objects.get(name="sahar")
                operator.send_message(message)

                h = {"text": "password sent", "status": 200}
                return Response({"text": "password sent", "status": 200}, headers=h)


class ChangeNumberSecond(CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        code = self.request.data.get('code', 0)
        newpn = self.request.data.get('phone', None)

        if usr.first_name == code and newpn:
            usr.username = newpn
            usr.save()
            user.phone = newpn
            user.save()

            return Response({'status': 200, "text": "شماره شما تغییر یافت.\nمجددا ورود کنید."},
                            headers={'status': 200, "text": "شماره شما تغییر یافت.مجددا ورود کنید."})
        else:
            return Response({"status": 400})


class ReportListView(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        rp_id = self.kwargs.get('rp_id')
        if rp_id == '__all__':
            return Report.objects.all()
        return Course.objects.filter(pk=rp_id)


class ReportCreateView(CreateAPIView):
    serializer_class = ReportSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        user = Profile.objects.get(user=usr)

        a = Report.objects.create(user=user, text=self.request.data.get('text', ' '))

        message = Message(token=a.text, to="+989379852503", token2="http://sessapp.moarefe98.ir/report/"+str(a.pk))

        operator = Operator.objects.get(name="sahar")
        operator.send_message(message)
        h = {"text": "report sent", "status": 200}
        return Response({"text": "report sent", "status": 200}, headers=h)


