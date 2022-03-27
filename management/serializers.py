from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = "__all__"


class ScheduleClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleClasses
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"

