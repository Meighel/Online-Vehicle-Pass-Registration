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

class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user_id"): #overrides the django dispatch
            return redirect("login")  #redirect to login if no active on session
        return super().dispatch(request, *args, **kwargs)
