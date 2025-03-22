from django.contrib import admin
from .models import (
    UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, VehiclePass,
    PaymentTransaction, InspectionReport, Notification, Announcement
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('corporate_email', 'firstname', 'lastname', 'program', 'department')
    search_fields = ('corporate_email', 'firstname', 'lastname')
    list_filter = ('program', 'department')



@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'badgeNumber', 'first_name', 'last_name', 'job_title')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'badgeNumber')
    list_filter = ('job_title',)

    def first_name(self, obj):
        return obj.user.firstname if obj.user else None
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.lastname if obj.user else None
    last_name.short_description = 'Last Name'


@admin.register(CashierProfile)
class CashierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cashier_id', 'first_name', 'last_name', 'job_title')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'cashier_id')
    list_filter = ('job_title',)

    def first_name(self, obj):
        return obj.user.firstname if obj.user else None
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.lastname if obj.user else None
    last_name.short_description = 'Last Name'



@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('get_corporate_email', 'admin_id', 'first_name', 'last_name')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'admin_id')

    def get_corporate_email(self, obj):
        return obj.user.corporate_email if obj.user else None
    get_corporate_email.short_description = 'Corporate Email'

    def first_name(self, obj):
        return obj.user.firstname if obj.user else None
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.lastname if obj.user else None
    last_name.short_description = 'Last Name'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'plateNumber', 'type', 'model', 'color')
    search_fields = ('plateNumber', 'owner__firstname', 'owner__lastname')
    list_filter = ('color', 'model', 'type')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registrationNumber', 'user', 'plate_number', 'status', 'files')
    search_fields = ('registrationNumber', 'user__firstname', 'user__lastname', 'plate_number__plateNumber')
    list_filter = ('status', 'user__department')


@admin.register(VehiclePass)
class VehiclePassAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'passNumber', 'passExpire', 'status')
    search_fields = ('passNumber', 'vehicle__plateNumber')
    list_filter = ('status',)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'registration', 'cashier', 'status', 'date_processed')
    search_fields = ('receipt_number', 'registration__registrationNumber', 'cashier__user__firstname')
    list_filter = ('status', 'date_processed')


@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'security', 'inspection_date', 'is_approved')
    search_fields = ('payment_number__registration__registrationNumber', 'security__user__firstname')
    list_filter = ('is_approved', 'inspection_date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'recipient', 'message', 'date', 'is_read')
    search_fields = ('message', 'recipient__corporate_email')
    list_filter = ('type', 'is_read', 'date')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_posted', 'posted_by')
    search_fields = ('title', 'posted_by__corporate_email')
    list_filter = ('date_posted',)
