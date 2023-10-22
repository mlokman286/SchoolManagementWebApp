from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

    USER =(
        (1,'admin'),
        (2,'staff'),
        (3,'students'),
    )
    user_type=models.CharField(choices=USER,max_length=50,default=1)
    profile_pic=models.ImageField(upload_to="media/profile_pic")

class CourseModel(models.Model):
    name=models.CharField(max_length=100)
    createat=models.DateTimeField(auto_now_add=True)
    updateat=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class SessionYearModel(models.Model):
    sessionStart=models.CharField(max_length=100)
    sessionEnd=models.CharField(max_length=100)
    def __str__(self):
        return self.sessionStart + "/" + self.sessionEnd
    

class StudentModel(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender = models.CharField(max_length=100)
    courseid = models.ForeignKey(CourseModel, on_delete=models.DO_NOTHING,default=1)  # Set the default course
    sessionyearid = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING,default=1)
    cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
class TeacherModel(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender = models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    courseid = models.ForeignKey(CourseModel, on_delete=models.DO_NOTHING,default=2)
    experience=models.CharField(max_length=100)
    cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)
       
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
class SubjectModel(models.Model):
    name=models.CharField(max_length=100)
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE)
    teacher=models.ForeignKey(TeacherModel,on_delete=models.CASCADE)
    cratedat = models.DateTimeField(auto_now_add=True, null=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name