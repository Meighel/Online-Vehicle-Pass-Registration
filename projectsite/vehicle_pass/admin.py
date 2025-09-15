# from django.contrib import admin
# from .models import (
#     UserProfile, SecurityProfile, CashierProfile, AdminProfile,
#     Vehicle, Registration, VehiclePass,
#     PaymentTransaction, InspectionReport,
#     Notification, Announcement, SiteVisit, LoginActivity, PasswordResetCode
# )


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('corporate_email', 'firstname', 'middle_name', 'lastname', 'suffix', 'program', 'department', 'address', 'role', 'school_role')
#     search_fields = ('corporate_email', 'firstname', 'lastname')
#     list_filter = ('program', 'department', 'role', 'school_role')


# @admin.register(SecurityProfile)
# class SecurityProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'badgeNumber', 'job_title', 'get_first_name', 'get_last_name')
#     search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'badgeNumber')
#     list_filter = ('job_title',)

#     def get_first_name(self, obj):
#         return obj.user.firstname if obj.user else None
#     get_first_name.short_description = 'First Name'
#     get_first_name.admin_order_field = 'user__firstname'

#     def get_last_name(self, obj):
#         return obj.user.lastname if obj.user else None
#     get_last_name.short_description = 'Last Name'
#     get_last_name.admin_order_field = 'user__lastname'

# @admin.register(CashierProfile)
# class CashierProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'cashier_id', 'get_first_name', 'get_last_name', 'job_title')
#     search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'cashier_id')
#     list_filter = ('job_title',)

#     def get_first_name(self, obj):
#         return obj.user.firstname if obj.user else None
#     get_first_name.short_description = 'First Name'
#     get_first_name.admin_order_field = 'user__firstname'

#     def get_last_name(self, obj):
#         return obj.user.lastname if obj.user else None
#     get_last_name.short_description = 'Last Name'
#     get_last_name.admin_order_field = 'user__lastname'

# @admin.register(AdminProfile)
# class AdminProfileAdmin(admin.ModelAdmin):
#     list_display = ('corporate_email', 'admin_id', 'get_first_name', 'get_last_name')
#     search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'admin_id')

#     def corporate_email(self, obj):
#         return obj.user.corporate_email if obj.user else None
#     corporate_email.short_description = 'Corporate Email'

#     def get_first_name(self, obj):
#         return obj.user.firstname if obj.user else None
#     get_first_name.short_description = 'First Name'
#     get_first_name.admin_order_field = 'user__firstname'

#     def get_last_name(self, obj):
#         return obj.user.lastname if obj.user else None
#     get_last_name.short_description = 'Last Name'
#     get_last_name.admin_order_field = 'user__lastname'

# @admin.register(PasswordResetCode)
# class PasswordResetCodeAdmin(admin.ModelAdmin):
#     list_display = ('user', 'code', 'expires_at', 'is_used')
#     search_fields = ('user', 'is_used')

# @admin.register(Vehicle)
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ('applicant', 'plateNumber', 'type', 'model', 'vehicle_color', 'chassisNumber', 'OR_Number', 'CR_Number', 'is_owner', 'owner_firstname', 'owner_middlename', 'owner_lastname', "owner_suffix", "relationship_to_owner", "contact_number")
#     search_fields = ('plateNumber', 'applicant__firstname', 'applicant__lastname')
#     list_filter = ('vehicle_color', 'model', 'type')


# @admin.register(Registration)
# class RegistrationAdmin(admin.ModelAdmin):
#     list_display = ('registrationNumber', 'user', 'vehicle', 'status', 'files', 'remarks', 'document_reviewed_by')
#     search_fields = ('registrationNumber', 'user__firstname', 'user__lastname')
#     list_filter = ('status', 'user__department')


# @admin.register(VehiclePass)
# class VehiclePassAdmin(admin.ModelAdmin):
#     list_display = ('vehicle', 'passNumber', 'passExpire', 'status', )
#     search_fields = ('passNumber', 'passExpire', 'vehicle__plateNumber')
#     list_filter = ('status',)


# @admin.register(PaymentTransaction)
# class PaymentTransactionAdmin(admin.ModelAdmin):
#     list_display = ('receipt_number', 'registration', 'cashier', 'status', 'due_date', 'date_processed', 'remarks')
#     search_fields = ('receipt_number', 'registration__registrationNumber', 'cashier__user__firstname')
#     list_filter = ('status', 'date_processed')


# @admin.register(InspectionReport)
# class InspectionReportAdmin(admin.ModelAdmin):
#     list_display = ('payment_number', 'security', 'document_inspection_date', 'physical_final_inspection_date', 'is_approved')
#     search_fields = ('payment_number__registration__registrationNumber', 'security__user__firstname')
#     list_filter = ('is_approved', 'document_inspection_date', 'physical_final_inspection_date')


# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('type', 'posted_by', 'message', 'date', 'is_read')
#     search_fields = ('message', 'posted_by__corporate_email')
#     list_filter = ('type', 'is_read', 'date')


# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
#     list_display = ('title', 'message', 'date_posted', 'posted_by')
#     search_fields = ('title', 'posted_by__corporate_email')
#     list_filter = ('date_posted',)

# @admin.register(SiteVisit)
# class SiteVisitAdmin(admin.ModelAdmin):
#     list_display = ('session_key', 'ip_address', 'user_agent', 'created_at')
#     search_fields = ('user_agent', 'created_at')

# @admin.register(LoginActivity)
# class LoginActivityAdmin(admin.ModelAdmin):
#     list_display = ('user', 'login_time')
#     search_fields = ('user', 'login_time')


from django.contrib import admin
from .models import (
    UserProfile, SecurityProfile, AdminProfile,
    Vehicle, Registration, VehiclePass,
    Notification, Announcement, SiteVisit, LoginActivity, PasswordResetCode
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'corporate_email', 'firstname', 'middle_name', 'lastname', 'suffix',
        'role', 'school_role', 'college', 'office_or_college', 'contact'
    )
    search_fields = ('corporate_email', 'firstname', 'lastname')
    list_filter = ('role', 'school_role', 'college', 'office_or_college')


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


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('corporate_email', 'admin_id', 'get_first_name', 'get_last_name')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'admin_id')

    def corporate_email(self, obj):
        return obj.user.corporate_email if obj.user else None
    corporate_email.short_description = 'Corporate Email'
    corporate_email.admin_order_field = 'user__corporate_email'

    def get_first_name(self, obj):
        return obj.user.firstname if obj.user else None
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__firstname'

    def get_last_name(self, obj):
        return obj.user.lastname if obj.user else None
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__lastname'


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expires_at', 'is_used')
    search_fields = ('user__corporate_email',)
    list_filter = ('is_used',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'applicant', 'plate_number', 'make_model', 'year_model',
        'color', 'type', 'engine_number', 'chassis_number'
    )
    search_fields = ('plate_number', 'applicant__firstname', 'applicant__lastname')
    list_filter = ('color', 'type', 'year_model')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'registration_number', 'user', 'vehicle', 'status',
        'files', 'remarks', 'initial_approved_by', 'final_approved_by',
        'date_of_filing', 'sticker_released_date'
    )
    search_fields = ('registration_number', 'user__firstname', 'user__lastname', 'vehicle__plate_number')
    list_filter = ('status', 'user__college', 'user__office_or_college')


@admin.register(VehiclePass)
class VehiclePassAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'passNumber', 'passExpire', 'status')
    search_fields = ('passNumber', 'vehicle__plate_number')
    list_filter = ('status', 'passExpire')


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


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'user_agent', 'created_at')
    search_fields = ('user_agent',)
    list_filter = ('created_at',)


@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time')
    search_fields = ('user__username',)
    list_filter = ('login_time',)
