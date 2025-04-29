from django.contrib import admin
from django.urls import path, include
from vehicle_pass import views
from vehicle_pass.views import (
    login_view, logout_view, signup_view,
<<<<<<< HEAD
    default_dashboard, security_dashboard, cashier_dashboard, admin_dashboard, 
    #admin_manage_user, admin_manage_application, admin_manage_payments,
=======
    #form1_view,
    default_dashboard, user_pass_status, user_application,
    vehicle_registration_step_1, vehicle_registration_step_2, vehicle_registration_step_3, 
    security_dashboard, SecurityViewApplication, SecurityViewSpecificApplication, SecurityViewStickers, 
    SecurityUpdateApplication, SecurityViewInspectionReports, security_report,
    handle_inspection_action,

    cashier_dashboard, cashierViewPayment, cashierUpdatePayment, cashierViewTransaction, cashier_report,
    admin_dashboard, AdminViewUser, AdminCreateUser, AdminUpdateUser, AdminDeleteUser, AdminViewSpecificUser,
    adminViewPayment, adminUpdatePayment, adminViewTransaction,
    #AdminViewApplication''', 
    AdminViewApplication, AdminViewSpecificApplication, AdminUpdateApplication,
    admin_manage_application, admin_manage_passes, admin_report,
    # admin_transaction, 
>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039
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
    path("dashboard/user/application/", user_application, name="user_application"),
    path("dashboard/user/application/step-1/", views.vehicle_registration_step_1, name="vehicle_registration_step_1"),
    path("dashboard/user/application/step-2/", views.vehicle_registration_step_2, name="vehicle_registration_step_2"),
    path("dashboard/user/application/step-3/", views.vehicle_registration_step_3, name="vehicle_registration_step_3"),
    path("dashboard/user/pass_status/", user_pass_status, name="user_pass_status"),
    
    
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/security/manage_application/", SecurityViewApplication.as_view(), name="security_manage_application"),
    path("dashboard/security/manage_application/<pk>/", SecurityUpdateApplication.as_view(), name="security_update_application"),
    path("dashboard/security/manage_application/view/<pk>", SecurityViewSpecificApplication.as_view(), name="security_view_specific_application"),
    path("dashboard/security/manage_inspection/", SecurityViewInspectionReports.as_view(), name="security_manage_inspection"),
    path("dashboard/security/manage_inspection/action/", handle_inspection_action, name='inspection_action'),
    path("dashboard/security/manage_stickers", SecurityViewStickers.as_view() , name="security_manage_stickers"),
    path("dashboard/security/manage_report/", security_report, name="security_report"),
    
    
    path("dashboard/cashier/", cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/cashier/cashier_payments/", cashierViewPayment.as_view(), name="cashier_payments"),
    path("dashboard/cashier/cashier_payments/<pk>/", cashierUpdatePayment.as_view(), name="cashier_update_payment"),  
    path("dashboard/cashier/cashier_transactions/", cashierViewTransaction.as_view(), name="cashier_transactions"),
    path("dashboard/cashier/cashier_reports/", cashier_report, name="cashier_reports"),

    
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
<<<<<<< HEAD

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
    path("dashboard/admin/manage_payments/add", AdminCreatePayment.as_view(), name="admin_create_payments"),
    path("dashboard/admin/manage_payments/<pk>/edit", AdminUpdatePayment.as_view(), name="admin_update_payments"),
    path("dashboard/admin/manage_payments/<pk>/delete", AdminDeletePayment.as_view(), name="admin_delete_payments"),
    #### admin passes
    path("dashboard/admin/manage_pass/", AdminViewPayment.as_view(), name="admin_manage_passes"),
    path("dashboard/admin/manage_pass/add", AdminCreatePayment.as_view(), name="admin_create_passes"),
    path("dashboard/admin/manage_pass/<pk>/edit", AdminUpdatePayment.as_view(), name="admin_update_passes"),
    path("dashboard/admin/manage_pass/<pk>/delete", AdminDeletePayment.as_view(), name="admin_delete_passes"),
    #### admin reports
    path("dashboard/admin/manage_report/", AdminViewPayment.as_view(), name="admin_manage_reports"),
    path("dashboard/admin/manage_report/add", AdminCreatePayment.as_view(), name="admin_create_reports"),
    path("dashboard/admin/manage_report/<pk>/edit", AdminUpdatePayment.as_view(), name="admin_update_reports"),
    path("dashboard/admin/manage_report/<pk>/delete", AdminDeletePayment.as_view(), name="admin_delete_reports"),

]
=======
    
    
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
    path("dashboard/admin/manage_report/", admin_report, name="admin_report"), path("dashboard/user/application/step-1/", views.vehicle_registration_step_1, name="vehicle_registration_step_1"),
    path("dashboard/user/application/step-2/", views.vehicle_registration_step_2, name="vehicle_registration_step_2"),
    path("dashboard/user/application/step-3/", views.vehicle_registration_step_3, name="vehicle_registration_step_3"),
    path("dashboard/user/application/complete/", views.registration_complete, name="registration_complete"),
]
>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039
