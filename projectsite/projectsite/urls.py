from django.contrib import admin
from django.urls import path, include
from vehicle_pass.views import (
    login_view, logout_view, signup_view,
    default_dashboard, security_dashboard, cashier_dashboard, 
    admin_dashboard, admin_manage_user, admin_manage_application, admin_manage_payments,
    home
)

from vehicle_pass.views import AdminCreateUser, AdminUpdateUser, AdminDeleteUser, AdminViewUser

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
    path("dashboard/admin/manage_users/", admin_manage_user, name="admin_manage_user"),
    path("dashboard/admin/manage_users/add", AdminCreateUser.as_view(), name="admin_create_user"),
    path("dashboard/admin/manage_users/<pk>/edit", AdminUpdateUser.as_view(), name="admin_update_user"),
    path("dashboard/admin/manage_users/<pk>/delete", AdminDeleteUser.as_view(), name="admin_delete_user"),

    #### admin application
    path("dashboaard/admin/manage_application/", admin_manage_application, name="admin_manage_application"),
    path("dashboaard/admin/manage_application/add", admin_manage_application, name="admin_create_application"),
    path("dashboaard/admin/manage_application/<pk>/edit", admin_manage_application, name="admin_update_application"),
    path("dashboaard/admin/manage_application/<pk>/delete", admin_manage_application, name="admin_delete_application"),
    #### admin payment
    path("dashboard/admin/manage_payments/", admin_manage_payments, name="admin_manage_payments"),


]
