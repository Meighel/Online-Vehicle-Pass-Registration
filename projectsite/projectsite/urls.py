from django.contrib import admin
from django.urls import path, include
from vehicle_pass.views import (
    login_view, logout_view, signup_view,
    default_dashboard, security_dashboard, cashier_dashboard, admin_dashboard, 
    #admin_manage_user, admin_manage_application, admin_manage_payments,
    home
)
from vehicle_pass.views import AdminCreateUser, AdminUpdateUser, AdminDeleteUser, AdminViewUser
from vehicle_pass.views import AdminCreateApplication, AdminUpdateApplication, AdminDeleteApplication, AdminViewApplication
from vehicle_pass.views import AdminCreatePayment, AdminUpdatePayment, AdminDeletePayment, AdminViewPayment
from vehicle_pass.views import AdminViewPasses, AdminCreatePasses, AdminUpdatePasses, AdminDeletePasses

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path("logout/", logout_view, name="logout"), 
    path("dashboard/user/", default_dashboard, name="default_dashboard"),
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),

    #### admin manage users####
    path("dashboard/admin/manage_users/", AdminViewUser.as_view(), name="admin_manage_user"),
    path("dashboard/admin/manage_users/add", AdminCreateUser.as_view(), name="admin_create_user"),
    path("dashboard/admin/manage_users/<pk>/edit", AdminUpdateUser.as_view(), name="admin_update_user"),
    path("dashboard/admin/manage_users/<pk>/delete", AdminDeleteUser.as_view(), name="admin_delete_user"),
    #### admin application
    path("dashboaard/admin/manage_application/", AdminViewApplication.as_view(), name="admin_manage_application"),
    path("dashboaard/admin/manage_application/add", AdminCreateApplication.as_view(), name="admin_create_application"),
    path("dashboaard/admin/manage_application/<pk>/edit", AdminUpdateApplication.as_view(), name="admin_update_application"),
    path("dashboaard/admin/manage_application/<pk>/delete", AdminDeleteApplication.as_view(), name="admin_delete_application"),
    #### admin payment
    path("dashboard/admin/manage_payments/", AdminViewPayment.as_view(), name="admin_manage_payments"),
    path("dashboard/admin/manage_payments/", AdminCreatePayment.as_view(), name="admin_create_payments"),
    path("dashboard/admin/manage_payments/", AdminUpdatePayment.as_view(), name="admin_update_payments"),
    path("dashboard/admin/manage_payments/", AdminDeletePayment.as_view(), name="admin_delete_payments"),
]
