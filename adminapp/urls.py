from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login, name='login'),
    # path('registration-success/', views.registration_success, name='registration_success'),
    path('logout/',views.logout_view, name='logout'),
    path('home/',views.Home, name='home'),
    
    
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/',views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/',views.student_dashboard, name='student_dashboard'),
    path('parent_dashboard/',views.parent_dashboard, name='parent_dashboard'),
    path('guest_dashboard/',views.guest_dashboard, name='guest_dashboard'),
    
    
    path('all_users_list/', views.all_users_list, name='all_users_list'),
    path('roles/', views.roles, name='roles'),
    path('search_and_select/', views.search_and_select, name='search_and_select'),
    
    
    #profiles
    # path('profile_view/', views.profile_view, name='profile_view'),
    
    path('profile_view/', views.profile_view, name='admin_profile'),
    path('student_profile/', views.profile_view, name='student_profile'),
    path('teacher_profile/', views.profile_view, name='teacher_profile'),
    # path('guest_profile/', views.profile_view, name='guest_profile'),
    path('parent_profile/',views.profile_view,name='parent_profile'),
    
    path('admin_register/', views.admin_register, name='admin_register'),
    
    path('profile/', views.profile_view, name='profile_view'),
    
    
    path('contact_us', views.contact_us, name='contact_us'),
    path('about_us', views.about_us, name='about_us'),
    # path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course_watch', views.course_watch, name='course_watch'),
    path('admin_approval_view', views.admin_approval_view, name='admin_approval'),
    path('instructor-list/', views.instructor_list, name='instructor_list'),
    path('student_list', views.student_list, name='student_list'),
    path('verified_results', views.get_verified_quiz_results, name='verified_results'),
    path('approve-guests/',views. guest_approval_view, name='guest_approval'),
    
    path('all_courses', views.all_courses, name='all_courses'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
        
]