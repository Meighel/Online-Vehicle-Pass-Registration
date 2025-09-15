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
    list_display = ('corporate_email', 'firstname', 'middle_name', 'lastname', 'suffix', 'college', 'program', 'workplace', 'contact', 'role', 'school_role')
    search_fields = ('corporate_email', 'firstname', 'lastname', 'contact')
    list_filter = ('college', 'workplace', 'role', 'school_role')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('corporate_email', 'password', 'firstname', 'middle_name', 'lastname', 'suffix', 'contact', 'address')
        }),
        ('Student Information', {
            'fields': ('college', 'program'),
            'classes': ('collapse',),
        }),
        ('Family Information (Students)', {
            'fields': ('father_name', 'father_contact', 'father_address', 'mother_name', 'mother_contact', 'mother_address', 'guardian_name', 'guardian_contact', 'guardian_address'),
            'classes': ('collapse',),
        }),
        ('Employee Information', {
            'fields': ('position', 'workplace'),
            'classes': ('collapse',),
        }),
        ('System Information', {
            'fields': ('role', 'school_role', 'created_at', 'updated_at')
        }),
    )


@admin.register(SecurityProfile)
class SecurityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'badgeNumber', 'job_title', 'get_first_name', 'get_last_name', 'get_email')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'badgeNumber')
    list_filter = ('job_title',)
    readonly_fields = ('created_at', 'updated_at')

    def get_first_name(self, obj):
        return obj.user.firstname if obj.user else None
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__firstname'

    def get_last_name(self, obj):
        return obj.user.lastname if obj.user else None
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__lastname'
    
    def get_email(self, obj):
        return obj.user.corporate_email if obj.user else None
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__corporate_email'


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'admin_id', 'get_first_name', 'get_last_name')
    search_fields = ('user__corporate_email', 'user__firstname', 'user__lastname', 'admin_id')
    readonly_fields = ('created_at', 'updated_at')

    def get_email(self, obj):
        return obj.user.corporate_email if obj.user else None
    get_email.short_description = 'Corporate Email'
    get_email.admin_order_field = 'user__corporate_email'

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
    list_display = ('user', 'code', 'expires_at', 'is_used', 'created_at')
    search_fields = ('user__corporate_email', 'code')
    list_filter = ('is_used', 'expires_at', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'get_applicant_name', 'make_model', 'year_model', 'color', 'type', 'get_owner_name')
    search_fields = ('plate_number', 'make_model', 'applicant__firstname', 'applicant__lastname', 'owner_firstname', 'owner_lastname')
    list_filter = ('type', 'color', 'year_model')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('applicant', 'make_model', 'plate_number', 'year_model', 'color', 'type', 'engine_number', 'chassis_number')
        }),
        ('Owner Information (if not applicant)', {
            'fields': ('owner_firstname', 'owner_middlename', 'owner_lastname', 'owner_suffix', 'relationship_to_owner', 'contact_number', 'address'),
            'classes': ('collapse',),
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_applicant_name(self, obj):
        if obj.applicant:
            return f"{obj.applicant.firstname} {obj.applicant.lastname}"
        return None
    get_applicant_name.short_description = 'Applicant'
    get_applicant_name.admin_order_field = 'applicant__lastname'
    
    def get_owner_name(self, obj):
        if obj.owner_firstname and obj.owner_lastname:
            return f"{obj.owner_firstname} {obj.owner_lastname}"
        return "Same as applicant"
    get_owner_name.short_description = 'Owner'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'get_user_name', 'get_vehicle_plate', 'status', 'date_of_filing', 'get_initial_approver', 'get_final_approver')
    search_fields = ('registration_number', 'user__firstname', 'user__lastname', 'vehicle__plate_number')
    list_filter = ('status', 'date_of_filing', 'user__school_role')
    readonly_fields = ('registration_number', 'date_of_filing', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Registration Information', {
            'fields': ('registration_number', 'user', 'vehicle', 'files', 'status', 'remarks', 'date_of_filing')
        }),
        ('Approval Information', {
            'fields': ('initial_approved_by', 'final_approved_by', 'sticker_released_date'),
        }),
        ('E-signature Information', {
            'fields': ('e_signature', 'printed_name', 'signature_date'),
            'classes': ('collapse',),
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_user_name(self, obj):
        return f"{obj.user.firstname} {obj.user.lastname}" if obj.user else None
    get_user_name.short_description = 'User'
    get_user_name.admin_order_field = 'user__lastname'
    
    def get_vehicle_plate(self, obj):
        return obj.vehicle.plate_number if obj.vehicle else None
    get_vehicle_plate.short_description = 'Vehicle Plate'
    get_vehicle_plate.admin_order_field = 'vehicle__plate_number'
    
    def get_initial_approver(self, obj):
        if obj.initial_approved_by:
            return f"{obj.initial_approved_by.user.firstname} {obj.initial_approved_by.user.lastname}"
        return None
    get_initial_approver.short_description = 'Initial Approver'
    
    def get_final_approver(self, obj):
        if obj.final_approved_by:
            return f"{obj.final_approved_by.user.firstname} {obj.final_approved_by.user.lastname}"
        return None
    get_final_approver.short_description = 'Final Approver'


@admin.register(VehiclePass)
class VehiclePassAdmin(admin.ModelAdmin):
    list_display = ('pass_number', 'get_vehicle_plate', 'get_vehicle_owner', 'pass_expire', 'status', 'get_user_role')
    search_fields = ('pass_number', 'vehicle__plate_number', 'vehicle__applicant__firstname', 'vehicle__applicant__lastname')
    list_filter = ('status', 'pass_expire')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_vehicle_plate(self, obj):
        return obj.vehicle.plate_number if obj.vehicle else None
    get_vehicle_plate.short_description = 'Vehicle Plate'
    get_vehicle_plate.admin_order_field = 'vehicle__plate_number'
    
    def get_vehicle_owner(self, obj):
        if obj.vehicle and obj.vehicle.applicant:
            return f"{obj.vehicle.applicant.firstname} {obj.vehicle.applicant.lastname}"
        return None
    get_vehicle_owner.short_description = 'Vehicle Owner'
    get_vehicle_owner.admin_order_field = 'vehicle__applicant__lastname'
    
    def get_user_role(self, obj):
        if obj.vehicle and obj.vehicle.applicant:
            return obj.vehicle.applicant.school_role
        return None
    get_user_role.short_description = 'User Role'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'get_posted_by', 'message_preview', 'date', 'is_read')
    search_fields = ('message', 'posted_by__corporate_email', 'posted_by__firstname', 'posted_by__lastname')
    list_filter = ('type', 'is_read', 'date')
    readonly_fields = ('date', 'created_at', 'updated_at')
    
    def get_posted_by(self, obj):
        if obj.posted_by:
            return f"{obj.posted_by.firstname} {obj.posted_by.lastname}"
        return "System"
    get_posted_by.short_description = 'Posted By'
    get_posted_by.admin_order_field = 'posted_by__lastname'
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_posted_by', 'date_posted', 'message_preview')
    search_fields = ('title', 'message', 'posted_by__corporate_email', 'posted_by__firstname', 'posted_by__lastname')
    list_filter = ('date_posted',)
    readonly_fields = ('date_posted', 'created_at', 'updated_at')
    
    def get_posted_by(self, obj):
        if obj.posted_by:
            return f"{obj.posted_by.firstname} {obj.posted_by.lastname}"
        return "System"
    get_posted_by.short_description = 'Posted By'
    get_posted_by.admin_order_field = 'posted_by__lastname'
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'user_agent_preview', 'created_at')
    search_fields = ('ip_address', 'user_agent', 'session_key')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
    def user_agent_preview(self, obj):
        return obj.user_agent[:50] + "..." if len(obj.user_agent) > 50 else obj.user_agent
    user_agent_preview.short_description = 'User Agent'


@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time')
    search_fields = ('user__username', 'user__email')
    list_filter = ('login_time',)
    readonly_fields = ('login_time',)