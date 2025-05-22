from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import Guest_ProfilePermissionForm
from .models import Guest_ProfilePermission,Guest
from adminapp.models import Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import Account
from .models import Guest,Guest_ProfilePermission


def guest_assign_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  # Get the student by Account model
    guest = get_object_or_404(Guest, user=account)
    
    try:
        guest = Guest.objects.get(user=account)
    except Guest.DoesNotExist:
        guest = None 

    if request.method == "POST":
        form = Guest_ProfilePermissionForm(request.POST)
        if form.is_valid():
            if guest:
                print(f"Updating permissions for {guest}")
                permissions, created = Guest_ProfilePermission.objects.get_or_create(guest=guest)
            else:
                permissions, created = Guest_ProfilePermission.objects.get_or_create(account=account)
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()   
            print("Permissions saved successfully!")

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('guest_success_page',user_id=user_id)  # Redirect to success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = None
        if guest:
            existing_permissions = Guest_ProfilePermission.objects.filter(guest=guest).first()
        else:
            existing_permissions = Guest_ProfilePermission.objects.filter(account=account).first()
        form = Guest_ProfilePermissionForm(instance=existing_permissions)

    return render(request, 'guest/guest_roles_form.html', {'form': form, 'user': guest})


def guest_success(request, user_id=None):
    guest = None
    permissions = None
    
    if user_id:
        account = get_object_or_404(Account, id=user_id)
        
        # Ensure you correctly fetch the student object
        guest = get_object_or_404(Guest, user=account)

        # Fetch the permissions linked to the student
        permissions = Guest_ProfilePermission.objects.filter(guest=guest).first()

    return render(request, 'guest/assign_permission.html', {
        'user': guest,
        'permissions': permissions
    })

@login_required
def profile_edit(request):
    if request.method == "POST":
        user = request.user
        
        guest = get_object_or_404(Guest, user=user)
        permissions = Guest_ProfilePermission.objects.filter(guest=guest).first()
        
        # Check if the user has edit permissions
        if not permissions or not permissions.can_edit:
            messages.error(request, "You do not have permission to edit this profile.")
            return redirect('guest_profile_view')
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save()
            messages.success(request, "Profile image updated successfully!")
            return redirect('guest_profile_view')
        
        # Update user fields
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)

        # Save the updated user data
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('guest_profile_view')

    return render(request, 'profile.html', {'user': user})


@login_required
def profile_delete(request):
    user = request.user

    guest = get_object_or_404(Guest, user=user)
    permissions = Guest_ProfilePermission.objects.filter(guest=guest).first()
    
    if not permissions or not permissions.can_delete:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('guest_profile_view')

    if request.method == "POST":
        # Check if the confirmation checkbox is checked
        if 'confirm_delete' in request.POST:
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('register')  # Redirect to home or login page
        else:
            messages.error(request, "Please confirm the deletion before proceeding.")
            return redirect('guest_profile_view')

    return render(request, 'confirm_delete.html', {'user': user})

