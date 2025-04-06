from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("/login")  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper

def session_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

# from django.http import HttpResponseForbidden
# from django.shortcuts import redirect

# class CustomLoginPermissionMixin:
#     required_permission = None  # e.g., 'can_access_dashboard'

#     def dispatch(self, request, *args, **kwargs):
#         # Check if the user is authenticated (custom logic if needed)
#         if not request.session.get('user_id'):
#             return redirect('your-login-url')

#         # Get your custom user from session or DB
#         user = self.get_custom_user(request)

#         # Check if the user has the required permission
#         if self.required_permission and not self.has_permission(user):
#             return HttpResponseForbidden("You do not have permission to view this page.")

#         return super().dispatch(request, *args, **kwargs)

#     def get_custom_user(self, request):
#         from your_app.models import YourUserModel
#         user_id = request.session.get('user_id')
#         return YourUserModel.objects.get(pk=user_id)

#     def has_permission(self, user):
#         # Your own logic, e.g., check a boolean field or a permission table
#         return self.required_permission in user.get_custom_permissions()