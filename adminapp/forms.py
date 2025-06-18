
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Account
from django import forms
from .models import Account

class RegistrationForms(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password','roles']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
            'roles': forms.Select(attrs={'class': 'form-control'}),
            }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")
        return cleaned_data




class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'profile_image']
        
    
#-----------------------------------------


class AdminUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('instructor', 'Instructor'), ('admin', 'Admin')])
    is_active = forms.BooleanField(required=False, initial=True)
    is_approved = forms.BooleanField(required=False)

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password1', 'password2', 'role', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        # Validate instructor-specific fields
        if role == 'instructor' and 'designation' not in cleaned_data:
            raise ValidationError('Designation is required for instructors.')
        
        return cleaned_data
