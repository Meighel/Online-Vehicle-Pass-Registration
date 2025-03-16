from django.contrib import admin
from .models import (
    CustomUser, UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, RegistrationStatus, VehiclePass,
    PaymentTransaction, InspectionReport, Notification, Announcement
)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('corporate_email', 'role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('corporate_email',)
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('corporate_email',)
    fields = ('corporate_email', 'role', 'is_active', 'is_staff', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'program', 'department')
    search_fields = ('user', 'user__corporate_email', 'firstname', 'lastname')
    list_filter = ('user__role','program', 'department')

@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'firstname', 'lastname', 'job_title')
    search_fields = ('user__corporate_email', 'firstname', 'lastname')
    list_filter = ('job_title',)

@admin.register(CashierProfile)
class CashierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'firstname', 'lastname', 'job_title')
    search_fields = ('user__corporate_email', 'firstname', 'lastname')
    list_filter = ('job_title',)

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'firstname', 'lastname')
    search_fields = ('user__corporate_email', 'firstname', 'lastname')
    list_filter = ('user__role',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'plateNumber', 'type', 'model', 'color')
    search_fields = ('plateNumber', 'owner__firstname', 'owner__lastname')
    list_filter = ('color', 'model', 'type')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('applicationNumber', 'user', 'vehicle', 'files')
    search_fields = ('applicationNumber', 'user__firstname', 'vehicle__plateNumber')
    list_filter = ('vehicle', 'user__department')

@admin.register(RegistrationStatus)
class RegistrationStatusAdmin(admin.ModelAdmin):
    list_display = ('registration', 'remarks')
    search_fields = ('registration__applicationNumber', 'remarks')
    list_filter = ('remarks', 'registration__user__department')

@admin.register(VehiclePass)
class VehiclePassAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'passNumber', 'passExpire', 'status')
    search_fields = ('passNumber', 'vehicle__plateNumber')
    list_filter = ('status',)

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'registration', 'cashier', 'status', 'date_processed')
    search_fields = ('receipt_number', 'registration__applicationNumber', 'cashier__firstname',)
    list_filter = ('status', 'date_processed')

@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = ('registration', 'security', 'inspection_date', 'is_approved')
    search_fields = ('registration__applicationNumber', 'security__firstname')
    list_filter = ('is_approved', 'inspection_date')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'message', 'date', 'is_read')
    search_fields = ('user__corporate_email', 'message')
    list_filter = ('type', 'is_read', 'date')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_posted', 'posted_by')
    search_fields = ('title', 'posted_by__corporate_email')
    list_filter = ('date_posted',)
