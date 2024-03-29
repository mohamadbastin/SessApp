"""SessApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken import views

from SessApp import settings
from sess_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('department/<department_id>', DepartmentView.as_view()),
    path('departmentcourse/<dp_id>', DepartmentCourseView.as_view()),
    path('usercourse/<cr_id>', UserCourseListView.as_view()),
    path('usercourse/create/<cs_id>', UserCourseCreateView.as_view()),
    path('usercourse/delete/<cs_id>', UserCourseDeleteView.as_view()),
    path('create-db/', CreateDatabaseView.as_view()),
    path('clean-db/', CleanDatabaseView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('course/<course_id>', CourseView.as_view()),
    path('profile/update/', UpdateProfileView.as_view()),
    path('profile/delete/', DeleteProfileView.as_view()),
    path('note/create/<cr_id>', NoteCreateView.as_view()),
    path('note/update/<nt_id>', NoteUpdateView.as_view()),
    path('note/delete/<nt_id>', NoteDeleteView.as_view()),
    path('exam/create/<cr_id>', ExamDateCreateView.as_view()),
    path('exam/update/<ex_id>', ExamDateUpdateView.as_view()),
    path('exam/delete/<ex_id>', ExamDateDeleteView.as_view()),
    path('changenumber/', ChangeNumberFirst.as_view()),
    path('verifycode/', ChangeNumberSecond.as_view()),
    path('report/create/', ReportCreateView.as_view()),
    path('report/<rp_id>', ReportListView.as_view()),
    path('policy/', PpView.as_view()),
    path('contact/', ContactView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
