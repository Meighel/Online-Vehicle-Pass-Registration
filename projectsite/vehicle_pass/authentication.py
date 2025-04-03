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