
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentProfilePermissionForm
from .models import Student_ProfilePermission,Student
from adminapp.models import Account,Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import Account
from .models import Student, Student_ProfilePermission,Categoriestheory
from teacher.models import UserCourses,Categories,CourseResource,Course
from teacher.views import get_course_data,get_top_instructors
from time import time
from django.db import transaction  
from teacher.models import Instructor

def student_assign_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  # Get the student by Account model
    student = get_object_or_404(Student, user=account)
    
    try:
        student = Student.objects.get(user=account)
    except Student.DoesNotExist:
        student = None 

    if request.method == "POST":
        form = StudentProfilePermissionForm(request.POST)
        if form.is_valid():
            if student:
                print(f"Updating permissions for {student}")
                permissions, created = Student_ProfilePermission.objects.get_or_create(student=student)
            else:
                permissions, created = Student_ProfilePermission.objects.get_or_create(account=account)
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()   
            print("Permissions saved successfully!")

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('student_success_page',user_id=user_id)  # Redirect to success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = None
        if student:
            existing_permissions = Student_ProfilePermission.objects.filter(student=student).first()
        else:
            existing_permissions = Student_ProfilePermission.objects.filter(account=account).first()
        form = StudentProfilePermissionForm(instance=existing_permissions)

    return render(request, 'student/student_roles_form.html', {'form': form, 'user': student})


def student_success(request, user_id=None):
    student = None
    permissions = None
    
    if user_id:
        account = get_object_or_404(Account, id=user_id)
        
        # Ensure you correctly fetch the student object
        student = get_object_or_404(Student, user=account)

        # Fetch the permissions linked to the student
        permissions = Student_ProfilePermission.objects.filter(student=student).first()

    return render(request, 'student/assign_permissions.html', {
        'user': student,
        'permissions': permissions
    })


@login_required
def profile_edit(request):
    if request.method == "POST":
        user = request.user
        
        student = get_object_or_404(Student, user=user)
        permissions = Student_ProfilePermission.objects.filter(student=student).first()
        
        # Check if the user has edit permissions
        if not permissions or not permissions.can_edit:
            messages.error(request, "You do not have permission to edit this profile.")
            return redirect('profile_view')
              
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save()
            messages.success(request, "Profile image updated successfully!")
            return redirect('profile_view')

        
        # Update user fields
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)

        # Save the updated user data
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile_view')

    return render(request, 'profile.html', {'user': user})


@login_required
def profile_delete(request):
    user = request.user

    # Ensure the student and permissions are correctly fetched
    student = get_object_or_404(Student, user=user)
    permissions = Student_ProfilePermission.objects.filter(student=student).first()
    
    if not permissions or not permissions.can_delete:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')

    if request.method == "POST":
        # Check if the confirmation checkbox is checked
        if 'confirm_delete' in request.POST:
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('register')  # Redirect to home or login page
        else:
            messages.error(request, "Please confirm the deletion before proceeding.")
            return redirect('profile_view')

    return render(request, 'confirm_delete.html', {'user': user})


def course_filter(request, category_id=None):
    print("Category ID:", category_id)  # Debug
    categories = Categories.objects.all().order_by('id')[:6]
    courses = Course.objects.filter(status="PUBLISH")
    
    if category_id:
        selected_category = get_object_or_404(Categories, id=category_id)
        courses = courses.filter(category=selected_category)
        print("Filtered Courses Count:", courses.count())  # Debug
    
    context = {
        'category': categories,
        'courses': courses,
        'selected_category': selected_category if category_id else None,
    }
    return render(request, 'student/course/course_filter.html', context)



def course_detail(request, course_id):
    course_data = get_course_data(course_id, request.user)   # another function, place just above
    return render(request, 'student/course/courses-detail.html', course_data)



def CHECKOUT(request, course_id):
    # Get the course
    course = Course.objects.get(pk=course_id)
    action = request.GET.get('action')
    order = None

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to the registration page
        return redirect('accounts/register')  # Replace 'registration_url' with your actual registration URL name

    # If the course is free
    if course.price == 0:
        usercourse = UserCourses(
            user=request.user,
            course=course
        )
        usercourse.save()
        messages.success(request, 'Course has successfully enrolled!')
        return redirect('my_course')

    # If action is to create payment
    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address = request.POST.get('address')
            
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')

            amount = (course.price) * 100
            currency = "INR"
            notes = {
                "name": f'{first_name} {last_name}',
                "country": country,
                "address": address,
                "city": city,
                "state": state,
                "postcode": postcode,
                "phone": phone,
                "email": email,
                "order_comments": order_comments,
            }
            receipt = f"Edu-{int(time())}"
            order = client.order.create({
                'receipt': receipt,
                'amount': amount,
                'currency': currency,
                'notes': notes,
            })

            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    context = {
        'course': course,
        'order': order,
    }
    
    return render(request, 'student/payment/checkout.html', context)


def MY_COURSE(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    enrolled_courses = UserCourses.objects.filter(user=request.user)
    category = Categories.objects.all().order_by('id')[:6]
    theory = Categoriestheory.objects.all().order_by('id')[:6]
    courser = CourseResource.get_all_category(CourseResource)

    context = {
        'enrolled_courses': enrolled_courses,
        'category': category,
        'theory': theory,
        'courser': courser,
    }
    print(enrolled_courses,category,theory,courser)
    
    return render(request, 'student/course/my-course.html', context)


def index(request):
    category=Categories.objects.all().order_by('id')[0:6]
    theory=Categoriestheory.objects.all().order_by('id')[0:6]
    course=Course.objects.filter(status='PUBLISH').order_by('-id')
    courser=CourseResource.get_all_category(CourseResource)
    
    top_teachers = get_top_instructors

    context={
        'category':category,
        'course':course,
        'theory':theory,
        'courser':courser, 
        'top_teachers':top_teachers,
    }
    return render(request,'index.html',context)


def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    is_enrolled = UserCourses.objects.filter(user=request.user, course=course).exists()
    if not is_enrolled:
        UserCourses.objects.create(user=request.user, course=course, paid=True)  # Or paid=False as needed

    return redirect('my_course')


def teachers_details(request, teacher_id):
    category=Categories.get_all_category(Categories).order_by('id')[0:6]


    teacher = get_object_or_404(Account,id = teacher_id)
    try:
        instructor = Instructor.objects.get(user = teacher)
        my_courses = Course.objects.filter(author = instructor)
        context={
            'category':category,
            'teacher':teacher,
            'instructor':instructor,
            'my_courses':my_courses
            }
    except:

        context={
            'category':category,
            'teacher':teacher,
            'instructor':None,
            'courses':None
            }
    
    return render(request,'teachers-details.html',context)
