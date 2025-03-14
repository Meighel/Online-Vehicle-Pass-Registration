from django.contrib import admin
from .models import (
    CustomUser, UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, RegistrationStatus, VehiclePass,
    PaymentStatus, Notification, Announcement
)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('corporate_email', 'role', 'is_active', 'is_staff', 'is_superuser')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'program', 'department')

@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'firstname', 'lastname', 'job_title')

@admin.register(CashierProfile)
class CashierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'firstname', 'lastname', 'job_title')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'firstname', 'lastname')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'plateNumber', 'type', 'model', 'color')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('applicationNumber', 'user', 'vehicle', 'files')

@admin.register(RegistrationStatus)
class RegistrationStatusAdmin(admin.ModelAdmin):
    list_display = ('registration', 'remarks')

@admin.register(VehiclePass)
class VehiclePassAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'passNumber', 'passExpire', 'status')

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('registration', 'cashier', 'status', 'date_processed')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'message', 'date', 'is_read')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_posted', 'posted_by')
