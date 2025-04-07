from django.contrib import admin
from django.urls import path, include
from vehicle_pass.views import (
    login_view, logout_view, signup_view,
    default_dashboard, 
    security_dashboard, security_manage_application, security_manage_inspection, security_manage_stickers, security_report,
    cashier_dashboard, cashierViewPayment, cashierUpdatePayment, cashierViewTransaction, cashier_report,
    admin_dashboard, adminViewPayment, admin_transaction, admin_manage_user, admin_manage_application, admin_manage_passes, admin_report,
    home
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path("logout/", logout_view, name="logout"), 
    path("dashboard/user/", default_dashboard, name="default_dashboard"),
    
    
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/security/manage_application/", security_manage_application, name="security_manage_application"),
    path("dashboard/security/manage_inspection/", security_manage_inspection, name="security_manage_inspection"),
    path("dashboard/security/manage_stickers", security_manage_stickers, name="security_manage_stickers"),
    path("dashboard/security/manage_report/", security_report, name="security_report"),
    
    
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/cashier/cashier_payments/", cashierViewPayment.as_view(), name="cashier_payments"),
    path("dashboard/cashier/cashier_payments/<pk>/", cashierUpdatePayment.as_view(), name="cashier_update_payment"),  
    path("dashboard/cashier/cashier_transactions/", cashierViewTransaction.as_view(), name="cashier_transactions"),
    path("dashboard/cashier/cashier_reports/", cashier_report, name="cashier_reports"),

    
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/manage_users/", admin_manage_user, name="admin_manage_user"),
    path("dashboaard/admin/manage_application/", admin_manage_application, name="admin_manage_application"),
    path("dashboard/admin/manage_payments/", adminViewPayment.as_view(), name="admin_payments"),
    path("dashboard/admin/manage_transactions/", admin_transaction, name="admin_transaction"),
    path("dashboard/admin/manage_passes/", admin_manage_passes, name="admin_manage_passes"),
    path("dashboard/admin/manage_report/", admin_report, name="admin_report"),
]