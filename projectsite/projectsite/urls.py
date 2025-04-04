from django.contrib import admin
from django.urls import path, include
from vehicle_pass.views import (
    login_view, logout_view, signup_view, 
    default_dashboard, security_dashboard, cashier_dashboard, 
    admin_dashboard, admin_manage_user,
    home
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"), 
    path("dashboard/user/", default_dashboard, name="default_dashboard"),
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/manage_user", admin_manage_user, name="admin_manage_user")
]
