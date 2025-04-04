from .models import UserProfile

def admin_user_context(request):
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            admin_user = UserProfile.objects.get(id=user_id, role='admin')
            admin_name = f"{admin_user.firstname} {admin_user.lastname}"
        except Exception as e:
            admin_name = "Admin"
    else:
        admin_name = "Not Logged In"
        
    return {'admin_name': admin_name}