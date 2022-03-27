from importlib import resources
import resource
from django.contrib import admin
from .models import School, User, Class, Subject, Period, ScheduleClasses, Attendence
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.db.models import Q
from django.urls import path, include
from . import views
# Register your models here.


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['school_id', 'school_name', 'school_address']

    def get_queryset(self, request):
        qs = super(SchoolAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(school_name=request.user.school_id)

    def get_actions(self, request):
        actions = super(SchoolAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ClassResource(resources.ModelResource):
    class Meta:
        model = Class
        fields = ('class_id', 'class_name')


@admin.register(Class)
class ClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['class_id', 'class_name', 'count_student', 'Timetable']
    resource_class = ClassResource

    def get_queryset(self, request):
        qs = super(ClassAdmin, self).get_queryset(request)

        if request.user.user_type == "Student":
            return qs.filter(class_name=request.user.class_id)
        return qs

    def count_student(self, obj):
        c1 = Q(class_id=obj.class_id)
        c2 = Q(user_type="Student")
        count = User.objects.filter(c1 & c2).count()
        return count

    def get_actions(self, request):
        actions = super(ClassAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def Timetable(self, obj):
        return format_html(f'<a href="/timetable/{obj.class_id}">Timetable</a>')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_id', 'subject_name']

    def get_actions(self, request):
        actions = super(SubjectAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time']

    def get_actions(self, request):
        actions = super(PeriodAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ScheduleClasses)
class ScheduleClassesAdmin(admin.ModelAdmin):
    list_display = ['date', 'class_id',
                    'teacher_id', 'subject_id', 'period_id']

    def get_actions(self, request):
        actions = super(ScheduleClassesAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        qs = super(ScheduleClassesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(class_id=request.user.class_id)    


class AttendenceResource(resources.ModelResource):
    class Meta:
        model = Attendence
        fields = ('student_id__username', 'date', 'status')

    def get_actions(self, request):
        actions = super(AttendenceResource, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Attendence)
class AttendenceAdmin(PeriodAdmin, ImportExportModelAdmin):
    list_display = ['date', 'student_id', 'status',
                    'schedule_class_id', 'is_approved', 'Approve', 'Decline']
    list_filter = ['date', 'schedule_class_id']
    actions = ['approved']
    resource_class = AttendenceResource
    readonly_fields = ('is_approved',)

    def get_actions(self, request):
        actions = super(AttendenceAdmin, self).get_actions(request)
        if request.user.user_type == "Student":
            del actions['approved']    
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def approved(self, request, queryset):
        queryset.update(status=True)
        queryset.update(is_approved=True)

    approved.short_description = "Approved Attendence"

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.user_type == "Teacher":
            return []
        return self.readonly_fields

    def get_queryset(self, request):
        qs = super(AttendenceAdmin, self).get_queryset(request)
        if request.user.is_superuser  or request.user.user_type == "SchoolAdmin": 
            return qs
        if request.user.user_type == "Teacher":
            return qs.filter(schedule_class_id__class_id=request.user.class_id)    
        return qs.filter(student_id=request.user.id)

    def Approve(self, obj):
        # if obj.user_type == ''
        return format_html(f'<a href="/approve/{obj.id}">approve</a>')

    def Decline(self, obj):
        return format_html(f'<a href="/decline/{obj.id}">decline</a>')

    def save_model(self, request, obj, form, change):
        if request.user.user_type == "Student":
            obj.student_id = request.user
        super(AttendenceAdmin, self).save_model(request, obj, form, change)

    def get_list_filter(self, request):
        if request.user.user_type == "Student":
            return "date",
        else:
            return "date", "schedule_class_id",

    def get_form(self, request, obj=None, **kwargs):
        if request.user.user_type == "Student":
            self.exclude = ('student_id',)  
        form = super(AttendenceAdmin, self).get_form(request, obj, **kwargs)  
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student_id":
            kwargs["queryset"] = User.objects.filter(user_type="Student")
        elif db_field.name=="schedule_class_id":
            print(request.user.class_id)
            print(ScheduleClasses.class_id)
            kwargs["queryset"] = ScheduleClasses.objects.filter(class_id=request.user.class_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CustomUserAdmin(UserAdmin):
    list_filter = ('user_type'),
    UserAdmin.add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',)
        }),
    )
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Enter Your Details',
            {
                'fields': (
                    'user_type',
                    'gender',
                    'profie_image',
                    'school_id',
                    'class_id'
                ),

            },
        ),
    )

    list_display = ['first_name', 'last_name',
                    'email', 'user_type', 'school_id']

    # def get_queryset(self, request):
    #     qs = super(CustomUserAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(school_id=request.user.school_id)


admin.site.register(User, CustomUserAdmin)
