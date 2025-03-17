from django.contrib import admin
from .models import (
    CustomUser, UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, VehiclePass,
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
    search_fields = ('user__corporate_email', 'firstname', 'lastname')
    list_filter = ('program', 'department')


@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    # We display the related UserProfile and custom methods for first and last names.
    list_display = ('user', 'badgeNumber', 'first_name', 'last_name', 'job_title')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'badgeNumber')
    list_filter = ('job_title',)

    def first_name(self, obj):
        return obj.user.firstname
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.lastname
    last_name.short_description = 'Last Name'


@admin.register(CashierProfile)
class CashierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cashier_id', 'first_name', 'last_name', 'job_title')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'cashier_id')
    list_filter = ('job_title',)

    def first_name(self, obj):
        return obj.user.firstname
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.lastname
    last_name.short_description = 'Last Name'


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_id', 'first_name', 'last_name')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'admin_id')
    # Removed invalid list_filter referencing user__role

    def first_name(self, obj):
        return obj.user.firstname
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.lastname
    last_name.short_description = 'Last Name'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'plateNumber', 'type', 'model', 'color')
    search_fields = ('plateNumber', 'owner__firstname', 'owner__lastname')
    list_filter = ('color', 'model', 'type')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    # Adjusted field names to match the model (registrationNumber, plate_number)
    list_display = ('registrationNumber', 'user', 'plate_number', 'files')
    search_fields = ('registrationNumber', 'user__firstname', 'plate_number__plateNumber')
    list_filter = ('user__department',)  # Filtering on a valid field from UserProfile


@admin.register(VehiclePass)
class VehiclePassAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'passNumber', 'passExpire', 'status')
    search_fields = ('passNumber', 'vehicle__plateNumber')
    list_filter = ('status',)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'registration', 'cashier', 'status', 'date_processed')
    search_fields = ('receipt_number', 'registration__registrationNumber', 'cashier__user__firstname',)
    list_filter = ('status', 'date_processed')


@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    # Changed list_display to use actual model fields; using payment_number instead of registration.
    list_display = ('payment_number', 'security', 'inspection_date', 'is_approved')
    search_fields = ('payment_number__registration__registrationNumber', 'security__user__firstname')
    list_filter = ('is_approved', 'inspection_date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # Removed 'user' from list_display since Notification does not have a user field.
    list_display = ('type', 'message', 'date', 'is_read')
    search_fields = ('message',)
    list_filter = ('type', 'is_read', 'date')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_posted', 'posted_by')
    search_fields = ('title', 'posted_by__corporate_email')
    list_filter = ('date_posted',)
