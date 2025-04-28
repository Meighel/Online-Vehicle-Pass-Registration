from django.contrib import admin
from .models import (
    UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, VehiclePass, Owner,
    PaymentTransaction, InspectionReport, Notification, Announcement
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('corporate_email', 'firstname', 'lastname', 'program', 'department')
    search_fields = ('corporate_email', 'firstname', 'lastname')
    list_filter = ('program', 'department')



@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'badgeNumber', 'job_title', 'get_first_name', 'get_last_name')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'badgeNumber')
    list_filter = ('job_title',)

    def get_first_name(self, obj):
        return obj.user.firstname if obj.user else None
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__firstname'

    def get_last_name(self, obj):
        return obj.user.lastname if obj.user else None
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__lastname'

@admin.register(CashierProfile)
class CashierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cashier_id', 'get_first_name', 'get_last_name', 'job_title')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'cashier_id')
    list_filter = ('job_title',)

    def get_first_name(self, obj):
        return obj.user.firstname if obj.user else None
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__firstname'

    def get_last_name(self, obj):
        return obj.user.lastname if obj.user else None
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__lastname'

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('corporate_email', 'admin_id', 'get_first_name', 'get_last_name')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'admin_id')

    def corporate_email(self, obj):
        return obj.user.corporate_email if obj.user else None
    corporate_email.short_description = 'Corporate Email'

    def get_first_name(self, obj):
        return obj.user.firstname if obj.user else None
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__firstname'

    def get_last_name(self, obj):
        return obj.user.lastname if obj.user else None
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__lastname'

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('self_ownership', 'legal_owner', 'plateNumber', 'type', 'model', 'color')
    search_fields = ('plateNumber', 'self_ownership__firstname', 'self_ownership__lastname','legal_owner__owner_firstname', 'legal_owner__owner_lastname',)
    list_filter = ('color', 'model', 'type')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registrationNumber', 'user', 'vehicle', 'status', 'files')
    search_fields = ('registrationNumber', 'user__firstname', 'user__lastname')
    list_filter = ('status', 'user__department')


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('owner_firstname', 'owner_middlename', 'owner_lastname', 'owner_suffix', 'owner_contact_number', 'relationship_to_owner')
    search_fields = ('owner_firstname', 'owner_middlename', 'owner_lastname','owner_contact_number', 'relationship_to_owner')
    list_filter = ('owner_firstname', 'owner_lastname', 'relationship_to_owner')
                     


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
    list_display = ('type', 'posted_by', 'message', 'date', 'is_read')
    search_fields = ('message', 'posted_by__corporate_email')
    list_filter = ('type', 'is_read', 'date')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'date_posted', 'posted_by')
    search_fields = ('title', 'posted_by__corporate_email')
    list_filter = ('date_posted',)
