from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import Parent_ProfilePermissionForm
from .models import Parent_ProfilePermission,Parent
from adminapp.models import Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import Account


def assign_parent_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  # Get the student by Account model
    parent = get_object_or_404(Parent, user=account)
    

    if request.method == "POST":
        form = Parent_ProfilePermissionForm(request.POST)
        if form.is_valid():
            permissions, created = Parent_ProfilePermission.objects.get_or_create(parent=parent)
              
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
            permissions.save()   
            
            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('success_page',user_id=user_id)  # Redirect to success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = Parent_ProfilePermission.objects.filter(parent=parent).first()
        form = Parent_ProfilePermissionForm(instance=existing_permissions)

    return render(request, 'parent/parent_roles_form.html', {'form': form, 'user': parent})


def parent_success(request, user_id=None):
    parent = None
    permissions = None
    
    if user_id:
        account = get_object_or_404(Account, id=user_id)
        parent = get_object_or_404(Parent, user=account)
        permissions = Parent_ProfilePermission.objects.filter(parent=parent).first()

    return render(request, 'parent/assign_permission.html', {
        'user': parent,
        'permissions': permissions
    })
