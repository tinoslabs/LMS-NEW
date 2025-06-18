from django import forms
from .models import Guest_ProfilePermission
from adminapp.models import Account

class Guest_ProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Guest_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete','manage_categories','create_categories',
                  'edit_categories','delete_categories','manage_Instructor','create_Instructor','edit_Instructor',
                  'delete_Instructor','manage_Levels','create_Levels','edit_Levels','delete_Levels','manage_Language',
                  'create_Language','edit_Language','delete_Language','manage_Course','create_Course','edit_Course',
                  'delete_Course','manage_Lesson','create_Lesson','edit_Lesson','delete_Lesson','manage_CourseResource',
                  'create_CourseResource','edit_CourseResource','delete_CourseResource','manage_What_u_learn',
                  'create_What_u_learn','edit_What_u_learn','delete_What_u_learn','manage_Requirements',
                  'create_Requirements','edit_Requirements','delete_Requirements','manage_VideoModels','create_VideoModels',
                  'edit_VideoModels','delete_VideoModels','manage_Quiz', 'create_Quiz', 'edit_Quiz', 'delete_Quiz'
                  ]
        