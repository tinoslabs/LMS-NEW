from django.urls import path
from . import views

urlpatterns = [
    path('assign_permissions/<int:user_id>/', views.assign_parent_permissions, name='assign_parent_permissions'),
    path('success_page/<int:user_id>/', views.parent_success, name='success_page'),
]