from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
from .forms import RegistrationForms,LoginForm,UserProfileForm
import random
from django.contrib.auth import logout,authenticate
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from.decorators import allowed_roles
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import json 

from django.contrib import messages
from .models import Account
from .forms import AdminUserForm

from student.models import Student
from  parent.models import Parent 
from guest.models import Guest
from teacher.models import Teacher

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def register(request):
    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']  
            last_name = form.cleaned_data['last_name']    
            email = form.cleaned_data['email']
            role = form.cleaned_data['roles']
            print(email)
            password = form.cleaned_data['password']
            print(password)
            username = email.split('@')[0]
            
            # Ensure username is unique
            base_username = username.lower()
            unique_username = base_username
            counter = 1
            while Account.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}{counter}"
                counter += 1
                
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")  # Added password length validation
                return redirect('register')    
                
            user_details = [first_name.lower(), last_name.lower(), email.split('@')[0].lower()]
            
            if any(detail in password.lower() for detail in user_details):
                messages.error(request, "Password should not contain your name, email, or username.")  # Prevents user info in password
                return redirect('register')
                            
            try:
                validate_password(password)  # Uses Django's built-in password validation for better security
            except ValidationError as e:
                messages.error(request, " ".join(e.messages))
                return redirect('register')
            
        
            common_passwords = ["password", "12345678", "qwerty123", "admin123", "welcome123"]
            if password.lower() in common_passwords:
                messages.error(request, "Password is too common. Please choose a stronger password.")  #Prevents common weak passwords
                return redirect('register')  
            
                      
            otp = generate_otp()
            
            request.session['user_data'] = json.dumps({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': unique_username,
                'password': password,
                'otp': otp,
                'roles': role
            })

            # Send OTP to user's email
            try:
                send_mail(
                    subject="Your OTP Verification Code",
                    message=f"Your OTP for account activation is {otp}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email. Verify your account.')
            except Exception as e:
                messages.error(request, f'Error sending OTP: {e}')
                return redirect('register')
            request.session['email'] = email
            return redirect('verify_otp')
    else:
        form = RegistrationForms()
    return render(request, 'registration/register.html', {'form': form})


def verify_otp(request):
    email = request.session.get('email')

    if not email:
        return redirect('register')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()  
        
        try:
            user_data = json.loads(request.session.get('user_data', '{}'))
            
            if not user_data or user_data.get('email') != email:
                messages.error(request, 'Invalid session. Please register again.')
                return redirect('register')
            
            stored_otp = user_data.get('otp')
            
            if stored_otp == otp_entered:

                user = Account.objects.create_user(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    username=user_data['username'],
                    password=user_data['password'],
                    otp=None,  # Clear OTP
                    roles=user_data['roles']
                )
                user.is_active = True
                user.is_verified = True
                user.save()
                
                # Clear session data after saving
                del request.session['user_data']
                del request.session['email']
                
                messages.success(request, 'Account verified successfully! Please log in.')
                return redirect('login')
            
                # return redirect('registration_success')
            else:
                messages.error(request, 'Invalid OTP. Try again.')
                print('Invalid OTP. Try again.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('register')

    return render(request, 'registration/verify_otp.html')


def registration_success(request):
    return render(request, 'registration/success.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f'{email},{password}')
            
            # Use 'username' instead of 'email' for authentication
            user = authenticate(request, email=email, password=password)
            
            if user:
                if not user.is_verified:
                    messages.error(request, 'Please verify your account first.')
                    print('Please verify your account first.')
                    return redirect('login')  # Redirect immediately to prevent further execution
                
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                
                # Redirect based on role
                if user.is_superadmin:
                    return redirect('admin_dashboard')
                elif user.roles == 'Teacher':
                    return redirect('teacher_dashboard')
                elif user.roles == 'student':
                    return redirect('student_dashboard')
                elif user.roles == 'Parent':
                    return redirect('parent_dashboard')  
                elif user.roles == 'guest':
                    return redirect('guest_dashboard')
                else:
                    return redirect('home')    
            else:
                messages.error(request, 'Invalid email or password.')
                print('Invalid email or password.') 
    else:
        form = LoginForm()   
    return render(request, 'registration/login1.html', {'form': form})




def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def Home(request):
    return render(request,'base/home.html')


def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

# def teacher_dashboard(request):
#     return render(request, 'dashboard/teacher_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher/teacher_dashboard.html')

def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')

def parent_dashboard(request):
    return render(request, 'dashboard/parent_dashboard.html')

def guest_dashboard(request):
    return render(request,'dashboard/guest_dashboard.html')


@login_required
@allowed_roles(['admin'])
def all_users_list(request):
    users = Account.objects.all()
    return render(request,'adminapp/all_user_list.html',{'users':users}) 


def roles(request):
    return render(request,'adminapp/roles_form.html')


User = get_user_model()
def search_and_select(request):
    
    keyword = request.GET.get('keyword', '').strip()
    user = None
    
    if keyword:
        try:
            user = Account.objects.get(user_key=keyword)
        except Account.DoesNotExist:
            user = None
    return render(request, 'adminapp/roles_form.html',{"user":user})


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            
            if request.user.roles == 'admin':
                return redirect('admin_profile')
            elif request.user.roles == 'student':
                return redirect('student_profile')
            elif request.user.roles == 'teacher':
                return redirect('teacher_profile') 
            elif request.user.roles == 'guest':
                return redirect('guest_profile')
            elif request.user.roles == 'parent':
                return redirect('parent_profile')
        else:
            print("Form is not valid:", profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=request.user)

    # Render a template based on the role
    if request.user.roles == 'admin':
        template_name = 'adminapp/admin_profile.html'
    elif request.user.roles == 'student':
        template_name = 'student/student_profile.html'
    elif request.user.roles == 'teacher':
        template_name = 'teacher/teacher_profile.html'
    elif request.user.roles == 'guest':
        template_name = 'guest/guest_profile.html'
    elif request.user.roles == 'parent':
        template_name = 'parent/parent_profile.html'
    else:
        template_name = 'teacher/teacher_profile.html'  # Fallback template for undefined roles

    context = {
        'profile_form': profile_form,
    }
    return render(request, template_name, context)


#---------------------------------------

def admin_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')  # Added phone number
        address = request.POST.get('address')            # Added address
        role = request.POST.get('role')    

        # Error handling
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('admin_registration')

        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('admin_registration')

        if Account.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('admin_registration')
        
        # Admin status handling
        is_admin = True if role == 'admin' else False

        # Creating Admin User
        user = Account.objects.create_superuser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        user.phone_number = phone_number
        user.address = address
        user.roles = role
        user.is_admin = is_admin
        user.save()
        
        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'parent':
            Parent.objects.create(user=user)
        elif role == 'guest':
            Guest.objects.create(user=user)
        elif role == 'teacher':
            Teacher.objects.create(user=user)

        messages.success(request, f'{role.capitalize()} registered successfully. Now assign permissions.')
        return redirect('search_and_select')+ f'?keyword={user.unique_key}'

    return render(request, 'admin_registration.html')


