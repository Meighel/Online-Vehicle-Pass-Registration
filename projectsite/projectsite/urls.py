from django.contrib import admin
from django.urls import path, include
from vehicle_pass.views import (
    login_view, logout_view,
    default_dashboard, security_dashboard, cashier_dashboard, admin_dashboard,
    home
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"), 
    path("dashboard/user/", default_dashboard, name="default_dashboard"),
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
]

