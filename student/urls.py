from django.urls import path
from . import views

urlpatterns = [
   path('assign_permissions/<int:user_id>/', views.student_assign_permissions, name='student_assign_permissions'),
   path('success_page/<int:user_id>/', views.student_success, name='student_success_page'),
   
   path('profile/edit/', views.profile_edit, name='profile_edit'),
   path('profile/delete/', views.profile_delete, name='profile_delete'),
   
   path('index/', views.index, name='index'),  
   path('my-course/',views.MY_COURSE,name='my_course'),
   path('course_filter/<int:category_id>/',views.course_filter,name='course_filter'),
   path('student/course_filter/', views.course_filter, name='course_filter_all'),
   path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
   path('checkout/<int:course_id>/',views.CHECKOUT,name='checkout'),
   
   path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
   path('teachers_details/<int:teacher_id>/', views.teachers_details, name='teachers_details'),
   
   path('quiz_selection/', views.quiz_selection, name='quiz_selection'),
   path('start_quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
   path('quiz/<int:quiz_id>/question/<int:question_index>/', views.quiz_question, name='quiz_question'),
   path('quiz/<int:quiz_id>/complete', views.quiz_complete, name='quiz_complete'),
   path('quiz-result/<int:quiz_result_id>/', views.quiz_result, name='quiz_result'),
   path('quiz_result_all', views.quiz_result_all, name='quiz_result_all'),
   path('all_certificates/', views.student_certificates, name='all_certificates'),

   path('teachers',views.teachers, name='teachers'),
   
]

   