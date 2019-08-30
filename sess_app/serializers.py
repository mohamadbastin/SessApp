from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.relations import StringRelatedField

from .models import *


class UserGetOrCreate(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone', ]


class CourseSerializer1(serializers.ModelSerializer):
    # def __init__(self):
    #     self.profiles = ProfileSerializer()

    class Meta:
        model = Course
        fields = ['pk', 'title', 'department', 'teacher', 'group', 'time_room', 'gender', 'final_time', 'cs_id',
                  ]


class ProfileSerializer1(serializers.ModelSerializer):
    # courses = CourseSerializer1(many=True)

    class Meta:
        model = Profile
        fields = ['pk', 'department', 'phone', 'name', 'picture']


class CourseSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer1(many=True)

    class Meta:
        model = Course
        fields = ['pk', 'title', 'department', 'teacher', 'group', 'time_room', 'gender', 'final_time', 'cs_id',
                  'profiles']


# CourseSerializer.profiles = ProfileSerializer()


class DepartmentSerializer(serializers.ModelSerializer):
    # courses = CourseSerializer(many=True)

    class Meta:
        model = Department
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['text', 'user_course', 'date']


class ExamDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDate
        fields = '__all__'


class UserCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer1()
    notes = NoteSerializer(many=True)
    exam_dates = ExamDateSerializer(many=True)

    class Meta:
        model = UserCourse
        fields = ['pk', 'course', 'notes', 'exam_dates']


class CreateDatabaseSerializer(serializers.Serializer):
    pwd = serializers.CharField(max_length=100)


class ProfileSerializer(serializers.ModelSerializer):
    # courses = CourseSerializer1(many=True)
    user_course = UserCourseSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['pk', 'department', 'phone', 'name', 'picture', 'user_course']
