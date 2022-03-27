from re import I
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import redirect, render
import reportlab
from reportlab.pdfgen import canvas
import io
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from datetime import datetime
from rest_framework import generics
import requests


# Create your views here.


class UserApi_modelViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ClassApi_modelViewset(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]


class ScheduleClassesApi_modelViewset(viewsets.ModelViewSet):
    queryset = ScheduleClasses.objects.all()
    serializer_class = ScheduleClassesSerializer
    permission_classes = [IsAuthenticated]


class AttendenceApi_modelViewset(viewsets.ModelViewSet):
    queryset = Attendence.objects.all()
    serializer_class = AttendenceSerializer
    permission_classes = [IsAuthenticated]


def attendence_decline(request, pk):
    if(request.user.user_type != "Student"):
        att_obj = Attendence.objects.get(id=pk)
        att_obj.status = False
        att_obj.is_approved = True
        att_obj.save()
        return redirect("/admin/management/attendence")
    else:
        return HttpResponse("You do not have permission to change status")


def attendence_approve(request, pk):
    if(request.user.user_type != "Student"):
        att_obj = Attendence.objects.get(id=pk)
        att_obj.status = True
        att_obj.is_approved = True
        att_obj.save()
        return redirect("/admin/management/attendence")
    else:
        return HttpResponse("You do not have permission to change status")


def show_timetable(request, class_id):
    sc_obj = ScheduleClasses.objects.filter(class_id=class_id)
    static_days = ['Monday', 'Tuesday', 'Wednesday',
                   'Thursday', 'Friday', 'Saturday']
    period = ['1st', '2nd', '3rd', '4th', '5th', '6th']
    data = []
    User_access = request.user.user_type
    for day in static_days:
        di = {}
        di['day'] = day
        for num in range(1, 7):
            f = False
            for item in sc_obj:
                d = item.date.strftime('%A')
                print(d,day,item.period_id.name[0],num)
                if d == day and int(item.period_id.name[0]) == num:
                    f = True
                    di[num] = str(item.teacher_id)+'('+str(item.subject_id)+')'
            if not f:
                di[num] = None
        data.append(di)

    return render(request, 'management/timetable.html', {'data': data, 'user': User_access})

# class Schedule(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ScheduleClassesSerializer

#     def get_queryset(self):
#         school_id = School.objects.get(school_name=self.kwargs['school_name'])
#         return ScheduleClasses.objects.filter(user_id__school_id=school_id,
#                                               class_id=self.kwargs['class_id'])

#     def schedule_view(request, id):
#         URL = f'http://127.0.0.1:8001/scheduleclasses_api/{request.user.school_id}/{id}/'
#         data = requests.get(url=URL,headers={'Authorization':'Bearer %s' % 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2OTI3OTg4LCJpYXQiOjE2NDU2MzE5ODgsImp0aSI6ImQ1OWQzYmYyZjY4YjQzNmM4MzdjMmIzNzgzNGQyZmQ3IiwidXNlcl9pZCI6MX0.YhG7db1F1-EYUKpROaBPne1aGXMr3nYh-_YOlN6ult8'}).json()
#         days=['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday']
#         context={}
#         for day in days:
#             di = {}
#             for num in range(1,7):
#                 f=False
#                 for j in range(0,len(data)):
#                     i = data[j]['date']
#                     dto = datetime.strptime(i, '%Y-%m-%d').date()
#                     d=dto.strftime('%A')
#                     if d == day and data[j]['period_id'] == num:
#                         subject_name = Subject.objects.get(pk=data[j]['subject_id'])
#                         teacher_name = User.objects.get(pk=data[j]['user_id'])
#                         di[num] = str(teacher_name) + '(' + str(subject_name) + ')'
#                         f = True
#                 if not f:
#                     di[num] = ""

#             context[day] = di

#             print(context)
#             for i in context:
#                 print(i)
#                 print(context[i])

#         return render(request,'management/timetable.html',context=context)
