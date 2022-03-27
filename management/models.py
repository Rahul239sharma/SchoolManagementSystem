from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Common(models.Model):
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(auto_now=True)
    is_active = models.BooleanField()

    class Meta:
        abstract = True


class School(Common):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=20)
    school_address = models.TextField()

    class Meta:
        db_table = 'School'

    def __str__(self):
        return self.school_name


class Class(Common):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Class'

    def __str__(self):
        return self.class_name


class User(AbstractUser):
    gender = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    user = (
        ("Student", "Student"),
        ("Teacher", "Teacher"),
        ("SchoolAdmin", "SchoolAdmin"),
    )
    gender = models.CharField(max_length=8, choices=gender)
    user_type = models.CharField(max_length=15, choices=user)
    profie_image = models.ImageField(upload_to="static/profile")
    school_id = models.ForeignKey(
        School, on_delete=models.CASCADE, null=True, blank=True)
    class_id = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'User'    


class Subject(Common):
    subject_id = models.IntegerField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    user_id = models.ManyToManyField(User)

    class Meta:
        db_table = 'Subject'

    def __str__(self):
        return self.subject_name


class Period(Common):
    name = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'Period'

    def __str__(self):
        return self.name


class ScheduleClasses(Common):
    date = models.DateField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="teacher")
    subject_id = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="subject")
    period_id = models.ForeignKey(Period, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ScheduleClasses'

    def __str__(self):
        return ("{}-{}".format(self.class_id, self.period_id))


class Attendence(Common):
    date = models.DateField()
    student_id = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, verbose_name="student")
    status = models.BooleanField()
    schedule_class_id = models.ForeignKey(
        ScheduleClasses, on_delete=models.CASCADE, verbose_name='Schedule Class')
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'Attendence'
