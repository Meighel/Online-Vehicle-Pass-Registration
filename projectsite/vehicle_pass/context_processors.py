from .models import UserProfile

def admin_user_context(request):
    profile = None
    user_id = request.session.get('user_id')
    if user_id:
        profile = UserProfile.objects.filter(id=user_id).first()
    return {'profile': profile}


def default_user_context(request):
    profile = None
    user_id = request.session.get('user_id')
    if user_id:
        profile = UserProfile.objects.filter(id=user_id).first()
    return {'profile': profile}

def security_user_context(request):
    profile = None
    user_id = request.session.get('user_id')
    if user_id:
        profile = UserProfile.objects.filter(id=user_id).first()
    return {'profile': profile}

