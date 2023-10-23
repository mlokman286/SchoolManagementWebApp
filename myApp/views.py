from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .EmaiBackEnd import emailbackEnd
from .models import CourseModel, CustomUser, SessionYearModel, StudentModel, SubjectModel, TeacherModel
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

# Create your views here.
def signupPage(request):
    error_messages = {
        'password_error': 'Password and Confirm Password not match',
        'username_error':'This username is already exits',
        'email_error':'This email is already exits'
    }
    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmpassword")
        if pass1!= pass2:
            messages.error(request, error_messages['password_error'])
        else:
            if CustomUser.objects.filter(username = uname):
                messages.error(request, error_messages['username_error'])
            elif CustomUser.objects.filter(email = email):
                messages.error(request, error_messages['email_error'])
            else:
                # Use your customUser model to create a user
                myuser = CustomUser.objects.create_user(username=uname, email=email, password=pass1)
                myuser.save()
                return redirect("loginPage")

    return render(request,'signup.html')

def loginPage(request):
    error_messages = {
        'username_error': 'Username is required.',
        'password_error': 'Password is required.',
        'login_error': 'Invalid username or password. Please try again.',
    }
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")  
        
        if not username:
            messages.error(request, error_messages['username_error'])
        elif not pass1:
            messages.error(request, error_messages['password_error'])
        else:
            user =authenticate(request, username=username, password=pass1,)

            if user is not None:
                login(request,user)
                user_type = user.user_type
                if user_type == '1':
                    return redirect("adminPage")
                elif user_type == '2':
                    # return render(request, "Staff/staffhome.html")
                    return HttpResponse("Teacher")
                elif user_type == '3':
                    # return render(request, "Students/Stustudenthome.html")
                    return HttpResponse("Student")
                else:
                    return redirect("signupPage")
            else:
                messages.error(request, error_messages['login_error'])

    return render(request,'login.html')

def adminPage(request):
    teacher = TeacherModel.objects.all().count
    student = StudentModel.objects.all().count
    department = CourseModel.objects.all().count
    subject = SubjectModel.objects.all().count
    context ={
        'teacher' : teacher,
        'student' : student,
        'department' : department,
        'subject' : subject,
    }
    return render(request,'myAdmin/adminhome.html',context)

def myProfile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

def profileUpdate(request):
    error_messages = {
        'success': 'Profile Update Successfully',
        'error': 'Profile Not Updated',
        'password_error': 'Current password is incorrect',
    }
    
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        try:
            cuser = CustomUser.objects.get(id=request.user.id)
            
            cuser.first_name = firstname
            cuser.last_name = lastname
            cuser.profile_pic = profile_pic
            
            # Verify the current password provided matches the user's current password
            if not cuser.check_password(password):
                messages.error(request, error_messages['password_error'])
            else:
                # If the current password is correct, proceed to update other fields
                if profile_pic is not None:
                    cuser.profile_pic = profile_pic
                # You can add additional fields to update here as needed
                cuser.save()
                messages.success(request, error_messages['success'])
                return redirect("profileUpdate")
        except:
            messages.error(request, error_messages['error'])
    
    return render(request, 'profile.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

def changePassword(request):
    error_messages = {
        'success': 'Changed Successfully',
        'mismatch': 'New password and confirm password not matched',
        'old_password': 'Old password not match',
    }
    if request.method == "POST":
        old_password = request.POST.get("oldPassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmPassword")
        user = request.user
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, error_messages['success'])
                logout(request)
                return redirect("loginPage")
            else:
                messages.error(request, error_messages['mismatch'])
        else:
            messages.error(request, error_messages['old_password'])
    return render(request,'changePassword.html')

def addStudent(request):
    error_messages = {
        'success': 'Student Add Successfully',
        'error': 'username or email already exist',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        session_year_id = request.POST.get("sessionyearid")

        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
            messages.error(request, error_messages['error'])
            
        else:
            # Create the customUser instance
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile_pic = profile_pic
            user.user_type = 3  # Assuming '3' represents students
            user.save()

            # Retrieve the selected course and session year
            myCourse = CourseModel.objects.get(id=course_id)
            mySessionYear = SessionYearModel.objects.get(id=session_year_id)

            # Create the student instance
            student = StudentModel(
                admin=user,
                address=address,
                sessionyearid=mySessionYear,
                courseid=myCourse,
                gender=gender,
            )
            # Save the student instance
            student.save() 
            messages.success(request, error_messages['success'])
            return redirect("studentList")
        
    course = CourseModel.objects.all()
    session = SessionYearModel.objects.all()
    st=StudentModel.objects.all()
    context = {
        'course':course,
        'session':session,
        'st':st
    }
    return render(request,'Student/addStudent.html',context)

def studentList(request):
    allStudent=StudentModel.objects.all()
    return render(request,'Student/studentlist.html',{'students':allStudent})

def editStudent(request,id):
    student=StudentModel.objects.filter(id=id)
    course = CourseModel.objects.all()
    session_year = SessionYearModel.objects.all()

    context = {
        "course": course,
        "session": session_year,
        "student":student,
        
    }

    return render(request,'Student/editStudent.html',context)

def updateStudent(request):
    error_messages = {
        'success': 'Student Updated Successfully',
        'error': 'Student Updated Failed',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        session_year_id = request.POST.get("sessionyearid")

        user=CustomUser.objects.get(id=student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.username=username

        if password is not None and password!="":
            user.set_password(password)
        if password is not None and profile_pic!="":
            user.profile_pic=profile_pic
        user.save()

        student=StudentModel.objects.get(admin=student_id)
        student.address=address
        student.gender=gender

        course=CourseModel.objects.get(id=course_id)
        student.course_id=course

        session=SessionYearModel.objects.get(id=session_year_id)
        student.session_year_id=session

        student.save()

        messages.success(request, error_messages['success'])
        return redirect("studentList")

    return render(request,"myAdmin/editStudent.html")

def addTeacher(request):
    error_messages = {
        'success': 'Teacher Add Successfully',
        'erroremail': 'email already exist',
        'errorusername': 'username already exist',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")

         # Check if email or username already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, error_messages['erroremail'])
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, error_messages['errorusername'])

        else:
            # Create the customUser instance
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile_pic = profile_pic
            user.user_type = 2  # Assuming '2' represents Teahcers
            # Save the user instance
            user.save()

            # Retrieve the selected course and session year
            myCourse = CourseModel.objects.get(id=course_id)
            teacher = TeacherModel(
                admin=user,
                address=address,
                courseid=myCourse,
                gender=gender,
                mobile=mobile,
                experience=experience,
            )
            # Save the Teacher instance
            teacher.save()
            messages.success(request, error_messages['success'])
            return redirect("teacherList")
        # Fetch the course and session year data to display in the form
    course = CourseModel.objects.all()
    # Tc=TeacherModel.objects.all()
    context = {
        "course": course,
    }

    return render(request,'teacher/addTeacher.html',context)

def teacherList(request):
    allTeacher=TeacherModel.objects.all()
    return render(request,'teacher/teacherList.html',{'teacher':allTeacher})

def editTeacher(request,id):
    teacher=TeacherModel.objects.filter(id=id)
    course = CourseModel.objects.all()
    context = {
        "course": course,
        "teacher":teacher,
    }
    
    return render(request,"teacher/editTeacher.html",context)

def updateTeacher(request):
    error_messages = {
        'success': 'Teacher Updated Successfully',
        'error': 'Teacher update Failed',
    }
    if request.method == "POST":
        teacher_id = request.POST.get("teacher_id")
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username") 
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")

        user=CustomUser.objects.get(id=teacher_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.username=username

        if password is not None and password!="":
            user.set_password(password)
        if password is not None and profile_pic!="":
            user.profile_pic=profile_pic
        user.save()

        teacher=TeacherModel.objects.get(admin=teacher_id)
        teacher.address=address
        teacher.gender=gender
        teacher.mobile=mobile
        teacher.experience=experience

        course=CourseModel.objects.get(id=course_id)
        teacher.course_id=course

        teacher.save()
        messages.success(request, error_messages['success'])
        return redirect("teacherList")
    
    return render(request,"teacher/editTeacher.html")

def addDepartment(request):
    error_messages = {
        'success': 'Department Add Successfully',
        'department_exist_error': 'Department already exist',
    }

    if request.method == "POST":
        department_name = request.POST.get("department_name")
        if CourseModel.objects.filter(name=department_name):
                messages.error(request, error_messages['department_exist_error'])
        else:
            course=CourseModel(   
                name=department_name,
            )
            course.save()
            messages.success(request, error_messages['success'])
            return redirect("departmentList")
        
    return render(request,'myAdmin/addDepartment.html')

def departmentList(request):
    department = CourseModel.objects.all()
    context = {
        "department": department,
    }
    return render(request,'myAdmin/departmentList.html',context)

def editDepartment(request,id):
    course = CourseModel.objects.get(id=id)
    context = {
        "course": course,
    }
    return render(request,'myAdmin/editDepartment.html',context)

def updateDepartment(request):
    error_messages = {
        'success': 'Department Updated Successfully',
        'error': 'Department Update Failed',
    }
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        department_name = request.POST.get("department_name")
        
        course=CourseModel.objects.get(id=department_id)
        course.name= department_name
        course.save()

        messages.success(request, error_messages['success'])
        return redirect("departmentList")
    else:
        messages.error(request, error_messages['error'])
        return redirect("editDepartment")
    
    # return render(request,"myAdmin/editDepartment.html")

def addSubject(request):
    course=CourseModel.objects.all()
    teacher=TeacherModel.objects.all()

    error_messages = {
        'success': 'Subject Add Successfully',
        'error':'Subject is Invalid',
        'subjecterror': 'Subject already exist',
    }
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        teacher_id = request.POST.get("teacher_id")
        subject_name = request.POST.get("subject_name")

        courseid=CourseModel.objects.get(id=course_id)
        teacherid=TeacherModel.objects.get(id=teacher_id)

        subject=SubjectModel(
            name=subject_name,
            course=courseid,
            teacher=teacherid,
        )
        subject.save()
        messages.success(request, error_messages['success'])
        return redirect("subjectList")
    
    context={
        "course":course,
        "teacher":teacher,
        } 

    return render(request,'myAdmin/addSubject.html',context)

def subjectList(request):
    subject = SubjectModel.objects.all()
    context = {
        'subject':subject
    }
    return render(request,'myAdmin/subjectList.html',context)

def editSubject(request,id):
    subject=SubjectModel.objects.filter(id=id)
    course=CourseModel.objects.all()
    teacher=TeacherModel.objects.all()

    context={
        
        "subject":subject,
        "course":course,
        "teacher":teacher,
    }
    return render(request,'myAdmin/editSubject.html',context)

def updateSubject(request):
    error_messages = {
        'success': 'Subject Update Successfully',
        'subjecterror': 'Subject Update Failed',
    }
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        course_id = request.POST.get("course_id")
        teacher_id = request.POST.get("teacher_id")
        subject_name = request.POST.get("subject_name")

        courseid=CourseModel.objects.get(id=course_id)
        teacherid=TeacherModel.objects.get(id=teacher_id)

        subject=SubjectModel(
        id=subject_id,
        name=subject_name,
        course=courseid,
        teacher=teacherid,
        )
        subject.save()
        messages.success(request, error_messages['success'])
        return redirect("subjectList")

    return render(request,'myAdmin/editSubject.html')

