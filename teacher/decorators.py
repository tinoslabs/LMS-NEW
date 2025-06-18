from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime


# def allowed_roles():
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_approved and request.user.role == 'student':
#                 raise PermissionDenied  # Deny access to unauthorized users
            
#             return view_func(request, *args, **kwargs)
            
#         return _wrapped_view
#     return decorator

from functools import wraps
from django.core.exceptions import PermissionDenied

def allowed_roles(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is an admin or superuser
            if 'admin' in roles and (request.user.roles == 'admin' or request.user.is_superadmin):
                return view_func(request, *args, **kwargs)
            
            # Check if user is an admin or instructor (case-insensitive)
            # if 'admin_and_instructor' in roles and (
            #     request.user.roles == 'admin' or 
            #     request.user.roles.lower() == 'instructor'
            # ):    
            if 'admin_and_instructor' in roles and (
                request.user.roles == 'admin' or 
                request.user.roles== 'Teacher'
            ):
                return view_func(request, *args, **kwargs)
            
            # Deny access if no condition is met
            raise PermissionDenied  
        
        return _wrapped_view
    return decorator



def otp_required(view_func):
    """
    A decorator to ensure the user has a valid OTP session and hasn't expired.
    """
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        otp_expiry = request.session.get('otp_expiry')

        # Check if user_id and otp_expiry exist in the session
        if not user_id or not otp_expiry:
            messages.error(request, "Session expired or unauthorized access. Please request an OTP again.")
            return redirect('request_otp_view')

        # try:

        otp_expiry_time = datetime.fromisoformat(otp_expiry)  # Handles +00:00 offset
        # except ValueError:
        #     messages.error(request, "Invalid OTP expiry format. Please request a new OTP.")
        #     return redirect('request_otp_view')

        # Check if OTP is expired
        if now() > otp_expiry_time:
            # Clear session variables if expired
            request.session.pop('user_id', None)
            request.session.pop('otp_expiry', None)
            messages.error(request, "OTP expired. Please request a new OTP.")
            return redirect('request_otp_view')

        # Proceed to the view if everything is valid
        return view_func(request, *args, **kwargs)
    return wrapper
