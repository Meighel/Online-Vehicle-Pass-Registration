from django.contrib import admin
from django.urls import path, include
from vehicle_pass import views 
from vehicle_pass.views import (
    login_view, logout_view, signup_view,
    default_dashboard, user_pass_status, user_application,
    security_dashboard, SecurityViewApplication, SecurityViewSpecificApplication, security_release_stickers, 
    SecurityUpdateApplication, security_report,

    admin_dashboard, AdminViewUser, AdminCreateUser, AdminUpdateUser, AdminDeleteUser, AdminViewSpecificUser,
    AdminViewApplication, AdminViewSpecificApplication, AdminUpdateApplication,
    admin_manage_application, admin_manage_passes, admin_report,

    
    #settings_view
    faq, about_us, contact_us,  # Add your views here
    home
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path('faq/', faq, name='faq'),
    path('about/', about_us, name='about'),
    path('contact/', contact_us, name='contact'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    path("dashboard/user/", default_dashboard, name="default_dashboard"),
    path("dashboard/user/application/", user_application, name="user_application"),
    path("dashboard/user/application/step-1/", views.vehicle_registration_step_1, name="vehicle_registration_step_1"),
    path("dashboard/user/application/step-2/", views.vehicle_registration_step_2, name="vehicle_registration_step_2"),
    path("dashboard/user/application/step-3/", views.vehicle_registration_step_3, name="vehicle_registration_step_3"),
    path("dashboard/user/pass_status/", user_pass_status, name="user_pass_status"),
    path('dashboard/user/settings/', views.settings_view, name='user_settings'),

    #user vehicle pass registration
    path("dashboard/user/application/step-1/", views.vehicle_registration_step_1, name="vehicle_registration_step_1"),
    path("dashboard/user/application/step-2/", views.vehicle_registration_step_2, name="vehicle_registration_step_2"),
    path("dashboard/user/application/step-3/", views.vehicle_registration_step_3, name="vehicle_registration_step_3"),
    path("dashboard/user/application/complete/", views.registration_complete, name="registration_complete"),
    
    
    path("dashboard/security/", security_dashboard, name="security_dashboard"),
    path("dashboard/security/manage_application/", SecurityViewApplication.as_view(), name="security_manage_application"),
    path("dashboard/security/manage_application/<pk>/", SecurityUpdateApplication.as_view(), name="security_update_application"),
    path("dashboard/security/manage_application/view/<pk>", SecurityViewSpecificApplication.as_view(), name="security_view_specific_application"),
    path("dashboard/security/manage_stickers", security_release_stickers, name="security_manage_stickers"),
    path("dashboard/security/manage_report/", security_report, name="security_report"),
    path('dashboard/security/settings/', views.settings_view, name='security_settings'),

    
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path('dashboard/admin/settings/', views.settings_view, name='admin_settings'),
    path('dashboard/admin/admin_reports/', views.admin_report, name='admin_reports'),

    #ADMIN USER CRUD
    path("dashboard/admin/manage_users/add/", AdminCreateUser.as_view(), name="admin_create_user"),
    path("dashboard/admin/manage_users/<pk>/", AdminUpdateUser.as_view(), name="admin_update_user"),
    path("dashboard/admin/manage_users/view/<pk>", AdminViewSpecificUser.as_view(), name="admin_view_specific_user"),
    path("dashboard/admin/manage_users/delete/<pk>/", AdminDeleteUser.as_view(), name="admin_delete_user"),
    path("dashboard/admin/manage_users/", AdminViewUser.as_view(), name="admin_manage_user"),

    #ADMIN APPLICATION CRUD
    path("dashboard/admin/manage_application/<pk>/", AdminUpdateApplication.as_view(), name="admin_update_application"),
    path("dashboard/admin/manage_application/view/<pk>", AdminViewSpecificApplication.as_view(), name="admin_view_specific_application"),    
    path("dashboard/admin/manage_application/", AdminViewApplication.as_view(), name="admin_manage_application"),
    
    path("dashboard/admin/manage_passes/", admin_manage_passes, name="admin_manage_passes"),
    path("dashboard/admin/manage_report/", admin_report, name="admin_report"),    

    path('api/notifications/', views.get_notifications_api, name='api_notifications'),
    path('api/notifications/<int:notification_id>/mark-read/', views.mark_notification_read_api, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', views.mark_all_read_api, name='mark_all_notifications_read'),
    path('api/notifications/count/', views.get_unread_count_api, name='unread_count'),
]