from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class School(models.Model):
    school_id=models.AutoField(primary_key=True)
    school_name=models.CharField(max_length=20)
    school_address=models.TextField()

class Class(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=50)  

class User(AbstractUser):
    gender = (
    ("Male", "Male"),
    ("Female","Female"),    
    ("Other","Other"),
)
    user = (
    ("Student", "Student"),
    ("Teacher","Teacher"),
)
    gender=models.CharField(max_length=8,choices=gender)
    user_type=models.CharField(max_length=8,choices=user)
    profie_image=models.ImageField()
    school_id=models.ForeignKey(School,on_delete=models.CASCADE,null=True,blank=True)
    class_id=models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)


class Subject(models.Model):
    subject_id = models.IntegerField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    user_id=models.ManyToManyField(User)


class Attendence(models.Model):
    date=models.DateField()
    student_id=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField()

class Period(models.Model):
    name=models.CharField(max_length=20)
    start_time=models.TimeField()
    end_time=models.TimeField()

class ScheduleClasses(models.Model):
    date=models.DateField()
    class_id=models.ForeignKey(Class,on_delete=models.CASCADE)   
    teacher_id=models.ForeignKey(User,on_delete=models.CASCADE)   
    subject_id=models.ForeignKey(Subject,on_delete=models.CASCADE)   
    period_id=models.ForeignKey(Period,on_delete=models.CASCADE)    
