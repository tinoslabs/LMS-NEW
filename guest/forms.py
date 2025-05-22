from django import forms
from .models import Guest_ProfilePermission
from adminapp.models import Account

class Guest_ProfilePermissionForm(forms.ModelForm):
    class Meta:
        model = Guest_ProfilePermission
        fields = ['can_manage', 'can_create', 'can_edit', 'can_delete']
        