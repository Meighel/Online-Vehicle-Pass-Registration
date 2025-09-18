from .models import UserProfile

def admin_user_context(request):
    profile = None
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            profile = UserProfile.objects.get(id=user_id, role='admin')
        except Exception:
            profile = None
    return {'profile': profile}

def default_user_context(request):
    profile = None
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            profile = UserProfile.objects.get(id=user_id, role='user')
        except Exception:
            profile = None
    return {'profile': profile}

def security_user_context(request):
    profile = None
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            profile = UserProfile.objects.get(id=user_id, role='security')
        except Exception:
            profile = None
    return {'profile': profile}