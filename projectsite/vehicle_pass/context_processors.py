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


def cashier_user_context(request):
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            cashier_user = UserProfile.objects.get(id=user_id, role='cashier')
            cashier_name = f"{cashier_user.firstname} {cashier_user.lastname}"
        except Exception as e:
            cashier_name = "Cashier"
    else:
        cashier_name = "Not Logged In"

    return {'cashier_name': cashier_name}

def default_user_context(request):
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            default_user = UserProfile.objects.get(id=user_id, role='user')
            user_name = f"{default_user.firstname} {default_user.lastname}"
        except Exception as e:
            user_name = "User"
    else:
        user_name = "Not Logged In"

    return {'user_name': user_name}

def security_user_context(request):
    if hasattr(request, 'session') and 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            security_user = UserProfile.objects.get(id=user_id, role='security')
            security_name = f"{security_user.firstname} {security_user.lastname}"
        except Exception as e:
            security_name = "Security"
    else:
        security_name = "Not Logged In"

    return {'security_name': security_name}