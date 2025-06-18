import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, otp=None, roles=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            user_key=self.generate_unique_alphanumeric_key(),
            otp=otp,
            roles=roles, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            roles='admin'
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_verified = True
        user.is_approved = True
        user.save(using=self._db)
        return user

    def generate_unique_alphanumeric_key(self):
        """ Ensure uniqueness of user_key by checking the database """
        while True:
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not self.model.objects.filter(user_key=key).exists():  # Corrected
                return key


CATEGORY_CHOICE=(
    # ('admin','admin'),
    ('student','student'),
    ('Teacher','Teacher'),
    ('Parent','Parent'),
    ('guest','guest'),
)

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=60, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default/default_profile.jpg', blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_key = models.CharField(max_length=10, unique=True, editable=False, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    roles = models.CharField(choices=CATEGORY_CHOICE,max_length=20)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()
        
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey('teacher.Course', on_delete=models.CASCADE, null=True)
    user_course = models.ForeignKey('teacher.UserCourses', on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " -- " + self.course.title
    