from django.db.models.signals import post_save
from django.dispatch import receiver
from adminapp.models import Account
from student.models import Student
from parent.models import Parent
from guest.models import Guest
from teacher.models import Teacher

@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    # Ensure related model is created for superusers
    if created or instance.is_superadmin:
        role = instance.roles.lower() if instance.roles else ""  # Normalize case
        
        if role == 'student':
            Student.objects.get_or_create(user=instance)
        elif role == 'teacher':
            Teacher.objects.get_or_create(user=instance)
        elif role == 'guest':
            Guest.objects.get_or_create(user=instance)
        elif role == 'parent':
            Parent.objects.get_or_create(user=instance)