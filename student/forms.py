from django import forms
from .models import Student_ProfilePermission
from adminapp.models import Account

class StudentProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Student_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete']
        
      