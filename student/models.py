from django.db import models
from adminapp.models import Account  # Importing the Account model
# from teacher.models import Courses

class Student(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="student_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# **Profile Permission Model**
class Student_ProfilePermission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="profile_permissions")
    can_manage = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} Profile Permissions"
    

class Categoriestheory(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default='default_value_here')
    def __str__(self):
        return self.name
    
    def get_all_theory(self):
        return Theory.objects.all().order_by('id') # type: ignore

