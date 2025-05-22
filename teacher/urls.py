from django.urls import path
from . import views
from .views import InstructorListView

urlpatterns = [

    path('teacher/assign_permissions/<int:user_id>/', views.assign_teacher_permissions, name='assign_teacher_permissions'),
    path('teacher/success_page/<int:user_id>/', views.teacher_success, name='teacher_success_page'),
    path('edit-teacher-permissions/<int:teacher_id>/', views.edit_teacher_permissions, name='edit_teacher_permissions'),
    # urls.py
    path('edit-teacher-permissions/<int:teacher_id>/', views.edit_teacher_permissions, name='edit_teacher_permissions'),
    
    path('profile/edit/', views.profile_edit, name='teacher_profile_edit'),
    path('profile/delete/', views.profile_delete, name='teacher_profile_delete'),
    
    path('add_category/', views.add_category, name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'), 
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    
    path('create_instructor',views.create_instructor, name='create_instructor'),
    path('Instructor_ListView',InstructorListView.as_view(), name='InstructorListView'),
    path('instructor/update/', views.update_instructor, name='update_instructor'),
    path('instructor/delete/', views.delete_instructor, name='delete_instructor'), 
    
    
    path('level_list', views.level_list, name='level_list'),
    path('add_level', views.add_level, name='add_level'),
    path('update_level/<int:pk>/', views.update_level, name='update_level'),
    path('delete_level/<int:pk>/', views.delete_level, name='delete_level'),
    
    
    # language
    path('add_language/', views.add_language, name='add_language'),
    path('language_list', views.language_list, name='language_list'),
    path('update_language/<int:pk>/', views.update_language, name='update_language'),
    path('delete_language/<int:pk>/', views.delete_language, name='delete_language'),


    #course
    path('add_course', views.add_course, name='add_course'),
    # path('courses/<int:course_id>/', views.course_detail, name='course_detail'),   #function testapp and used in both admin and lecture
    path('course_list/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/edit/', views.update_course, name='update_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),

    
    # course lesson 
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('update_lesson/<int:lesson_id>/', views.update_lesson, name='update_lesson'),
    path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),



        # course resources 
    path('resources/add/', views.add_course_resource, name='add_resource'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/update/<int:resource_id>/', views.update_course_resource, name='update_resource'),
    path('resources/delete/<int:resource_id>/', views.delete_course_resource, name='delete_resource'),
    
    
    #what you learn
    path('add_what_u_learn/', views.add_what_u_learn, name='add_what_u_learn'),
    path('what_u_learn_list/', views.what_u_learn_list, name='what_u_learn_list'),
    path('update_what_u_learn/edit/<int:entry_id>/', views.update_what_u_learn, name='update_what_u_learn'),
    path('delete_what_u_learn/<int:entry_id>/', views.delete_what_u_learn, name='delete_what_u_learn'),
    
    
    
    
    # course requirement
    path('add_requirement/', views.add_requirement, name='add_requirement'),
    path('requirement_list/', views.requirement_list, name='requirement_list'),
    path('update_requirement/<int:requirement_id>/', views.update_requirement, name='update_requirement'),
    path('delete_requirement/<int:requirement_id>/', views.delete_requirement, name='delete_requirement'),
    
    
    # course video file
    path('create_video',views.create_video, name='create_video'),
    path('view_video',views.view_video, name='view_video'),
    path('video_update/<int:video_id>/',views.video_update, name='video_update'),
    path('delete_videos/<int:video_id>/', views.delete_videos, name='delete_videos'),
    
    
    # quiz crud
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_questions/', views.add_questions, name='add_questions'),
    path('list_quiz/', views.list_quiz, name='list_quiz'),
    path('delete_quiz/<int:quiz_id>', views.delete_quiz, name='delete_quiz'),
    path('edit_quiz/<int:quiz_id>', views.edit_quiz, name='edit_quiz'),
    
    
    # quiz results
    path('quiz_results/<int:quiz_id>', views.get_quiz_results_for_course, name='quiz_results'),
    path('verify_result/<int:quiz_result_id>', views.verify_result, name='verify_result'),

]
