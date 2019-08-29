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
from django.urls import path
from rest_framework.authtoken import views
from sess_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', SignupView.as_view()),
    path('department/<department_id>', DepartmentView.as_view()),
    path('usercourse/<uc_id>', UserCourseListView.as_view()),
    path('create-db/', CreateDatabaseView.as_view()),
    path('profile/<pr_id>', ProfileView.as_view()),
    path('course/<course_id>', CourseView.as_view())
]
