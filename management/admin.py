from django.contrib import admin
from .models import School,User,Class,Subject,Period,ScheduleClasses,Attendence
# Register your models here.

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display=['school_id','school_name','school_address']
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','username','email','user_type']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
        list_display=['class_id','class_name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
        list_display=['subject_id','subject_name']

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
        list_display=['name','start_time','end_time']

@admin.register(ScheduleClasses)
class ScheduleClassesAdmin(admin.ModelAdmin):
        list_display=['date','class_id','teacher_id','subject_id','period_id']

@admin.register(Attendence)
class AttendenceAdmin(admin.ModelAdmin):
        list_display=['date','student_id','status']