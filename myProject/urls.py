from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signupPage,name='signupPage'),
    path('loginPage', views.loginPage,name='loginPage'),
    path('logoutPage', views.logoutPage,name='logoutPage'),

    # admin Panel
    path('adminPage', views.adminPage,name='adminPage'),
    path('myProfile/', views.myProfile,name="myProfile"), 
    path('myProfile/profileUpdate/', views.profileUpdate,name="profileUpdate"),
    path('myProfile/changePassword/', views.changePassword,name="changePassword"),

    # student panel
    path('adminPage/addStudent', views.addStudent,name='addStudent'),
    path('adminPage/studentList/editStudent/<str:id>', views.editStudent,name='editStudent'),
    path('adminPage/updateStudent/', views.updateStudent,name='updateStudent'),
    path('adminPage/studentList', views.studentList,name='studentList'),

    # Teacher Panel
    path('adminPage/addTeacher', views.addTeacher,name='addTeacher'),
    path('adminPage/teacherList', views.teacherList,name='teacherList'),
    path('adminPage/teacherList/editStudent/<str:id>', views.editTeacher,name='editTeacher'),
    path('adminPage/updateTeacher', views.updateTeacher,name='updateTeacher'),

    # Department Panel
    path('adminPage/addDepartment', views.addDepartment,name='addDepartment'),
    path('adminPage/departmentList', views.departmentList,name='departmentList'),
    path('adminPage/editDepartment/<str:id>', views.editDepartment,name='editDepartment'),
    path('adminPage/updateDepartment', views.updateDepartment,name='updateDepartment'),
    # Subject Panel
    path('adminPage/addSubject', views.addSubject,name='addSubject'),
    path('adminPage/subjectList', views.subjectList,name='subjectList'),
    path('adminPage/editSubject/<str:id>', views.editSubject,name='editSubject'),
    path('adminPage/updateSubject', views.updateSubject,name='updateSubject'),
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)