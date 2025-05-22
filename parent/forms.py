from django import forms
from .models import Parent_ProfilePermission

class Parent_ProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Parent_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete']