from django.contrib import admin
from myApp.models import CourseModel, CustomUser, SessionYearModel, StudentModel, SubjectModel, TeacherModel
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserModel(UserAdmin):
    list_display=['username','user_type']

admin.site.register(CustomUser,UserModel)
admin.site.register(CourseModel)
admin.site.register(SessionYearModel)
admin.site.register(StudentModel)
admin.site.register(TeacherModel)
admin.site.register(SubjectModel)