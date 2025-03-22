from django.urls import path
from .views import login_view, security_dashboard, cashier_dashboard, admin_dashboard

urlpatterns = [
    path("login/", login_view, name="login"),
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
]