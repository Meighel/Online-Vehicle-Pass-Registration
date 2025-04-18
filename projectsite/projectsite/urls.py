from django.contrib import admin
from django.urls import path, include
from vehicle_pass.views import (
    login_view, logout_view, signup_view,
    default_dashboard, 
    security_dashboard, SecurityViewApplication, SecurityViewSpecificApplication, SecurityUpdateApplication, security_manage_inspection, security_manage_stickers, security_report,
    cashier_dashboard, cashierViewPayment, cashierUpdatePayment, cashierViewTransaction, cashier_report,
    admin_dashboard, AdminViewUser, AdminCreateUser, AdminUpdateUser, AdminDeleteUser, AdminViewSpecificUser,
    adminViewPayment, adminUpdatePayment, adminViewTransaction,
    #AdminViewApplication''', 
    AdminViewApplication, AdminViewSpecificApplication, AdminUpdateApplication,
    admin_manage_application, admin_manage_passes, admin_report,
    # admin_transaction, 
    form1_view,
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
    path("dashboard/security/manage_application/", SecurityViewApplication.as_view(), name="security_manage_application"),
    path("dashboard/security/manage_application/<pk>/", SecurityUpdateApplication.as_view(), name="security_update_application"),
    path("dashboard/security/manage_application/view/<pk>", SecurityViewSpecificApplication.as_view(), name="security_view_specific_application"),
    path("dashboard/security/manage_inspection/", security_manage_inspection, name="security_manage_inspection"),
    path("dashboard/security/manage_stickers", security_manage_stickers, name="security_manage_stickers"),
    path("dashboard/security/manage_report/", security_report, name="security_report"),
    
    
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/cashier/cashier_payments/", cashierViewPayment.as_view(), name="cashier_payments"),
    path("dashboard/cashier/cashier_payments/<pk>/", cashierUpdatePayment.as_view(), name="cashier_update_payment"),  
    path("dashboard/cashier/cashier_transactions/", cashierViewTransaction.as_view(), name="cashier_transactions"),
    path("dashboard/cashier/cashier_reports/", cashier_report, name="cashier_reports"),

    
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path('form1/', form1_view, name='form1'),
    
    #ADMIN USER CRUD
    path("dashboard/admin/manage_users/add/", AdminCreateUser.as_view(), name="admin_create_user"),
    path("dashboard/admin/manage_users/<pk>/", AdminUpdateUser.as_view(), name="admin_update_user"),
    path("dashboard/admin/manage_users/view/<pk>", AdminViewSpecificUser.as_view(), name="admin_view_specific_user"),
    path("dashboard/admin/manage_users/delete/<pk>/", AdminDeleteUser.as_view(), name="admin_delete_user"),
    path("dashboard/admin/manage_users/", AdminViewUser.as_view(), name="admin_manage_user"),

    #ADMIN PAYMENT CRUD
    path("dashboard/admin/admin_payments/", adminViewPayment.as_view(), name="admin_payments"),
    path("dashboard/admin/admin_payments/<pk>/", adminUpdatePayment.as_view(), name="admin_update_payment"), 
    path("dashboard/admin/admin_transaction/", adminViewTransaction.as_view(), name="admin_transaction"),

    #ADMIN APPLICATION CRUD
    path("dashboard/admin/manage_application/<pk>/", AdminUpdateApplication.as_view(), name="admin_update_application"),
    path("dashboard/admin/manage_application/view/<pk>", AdminViewSpecificApplication.as_view(), name="admin_view_specific_application"),    
    path("dashboard/admin/manage_application/", AdminViewApplication.as_view(), name="admin_manage_application"),
    
    path("dashboard/admin/manage_passes/", admin_manage_passes, name="admin_manage_passes"),
    path("dashboard/admin/manage_report/", admin_report, name="admin_report"),
]