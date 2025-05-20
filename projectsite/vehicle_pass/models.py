from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import pytz
import random
import string
from datetime import timedelta


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    ROLE_CHOICES = [('user', 'User'),
        ('security', 'Security'),
        ('cashier', 'Cashier'),
        ('admin', 'Admin')
        ]
    
    SCHOOL_ROLE_CHOICES = [('student', 'Student'),
                   ('faculty', 'Faculty'),
                   ('university personnel', 'University Personnel')
                   ]
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    corporate_email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    lastname = models.CharField(max_length=25) 
    firstname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=25, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    dl_number = models.CharField(max_length=15, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', null=True)
    school_role = models.CharField(max_length=20, choices=SCHOOL_ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256$"):  # Prevent double hashing
            self.password = make_password(self.password)  # Hash password before saving
            
        super().save(*args, **kwargs)

        # Create profile based on role if not already existing
        if self.role == 'security' and not hasattr(self, 'securityprofile'):
            SecurityProfile.objects.create(user=self)
        elif self.role == 'cashier' and not hasattr(self, 'cashierprofile'):
            CashierProfile.objects.create(user=self)
        elif self.role == 'admin' and not hasattr(self, 'adminprofile'):
            AdminProfile.objects.create(user=self)


    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Check password

class SecurityProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    badgeNumber = models.CharField(max_length=10)
    job_title = models.CharField(max_length=30)

    def __str__(self):
        return f"Security Personnel: {self.user.firstname} {self.user.lastname} {self.badgeNumber}"  

class CashierProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    cashier_id = models.CharField(max_length=15)
    job_title = models.CharField(max_length=40)

    def __str__(self):
        return f"Cashier: {self.user.firstname} {self.user.lastname} {self.cashier_id}"  

class AdminProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    admin_id = models.CharField(max_length=15)

    def __str__(self):
        return f"Admin: {self.user.firstname} {self.user.lastname} ({self.admin_id})"

class PasswordResetCode(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reset code for {self.user.corporate_email}"
    
    def save(self, *args, **kwargs):
        # Set expiration time to 10 minutes from now if it's a new object
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    @classmethod
    def generate_code(cls):
        """Generate a random 4-digit code"""
        return ''.join(random.choices(string.digits, k=4))
    
    def is_valid(self):
        """Check if the code is still valid (not expired and not used)"""
        return not self.is_used and timezone.now() < self.expires_at
    

class Vehicle(BaseModel):
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    plateNumber = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    vehicle_color = models.CharField(max_length=20)
    chassisNumber = models.CharField(max_length=17)
    OR_Number = models.CharField(max_length=15)
    CR_Number = models.CharField(max_length=9)
    is_owner = models.BooleanField(default=False)
    
    # Only relevant if not the owner
    owner_firstname = models.CharField(max_length=45, null=True, blank=True)
    owner_middlename = models.CharField(max_length=45, null=True, blank=True)
    owner_lastname = models.CharField(max_length=45, null=True, blank=True)
    owner_suffix = models.CharField(max_length=5, null=True, blank=True)
    relationship_to_owner = models.CharField(max_length=15, null=True, blank=True)
    contact_number = models.CharField(max_length=13, null=True, blank=True)

    def __str__(self):
        return f"{self.plateNumber}"  

    def clean(self):
        if Vehicle.objects.filter(applicant=self.applicant).count() >= 2:
            raise ValidationError({'Applicant': 'You can only register up to two vehicles.'})

        if self.is_owner:
            if any([self.owner_firstname, self.owner_lastname, self.relationship_to_owner, self.contact_number]):
                raise ValidationError("Owner fields should be empty if you are the vehicle owner.")
        else:
            if not all([self.owner_firstname, self.owner_lastname, self.relationship_to_owner, self.contact_number]):
                raise ValidationError("Complete owner details are required if you're not the owner.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Registration(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('for payment', 'For Payment'),
        ('reviewing documents', 'Reviewing Documents'),
        ('for final inspection', 'For Final Inspection'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    registrationNumber = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    files = models.URLField(max_length=250)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(null=True)
    document_reviewed_by = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Registration {self.registrationNumber} for {self.user.lastname}, {self.user.firstname}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        if self.status == "for payment":
            payment, created = PaymentTransaction.objects.get_or_create(
                registration=self,
                defaults={
                    'status': 'pending',
                }
            )
            if created:
                payment.save() 

class VehiclePass(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked')
    ]
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    passNumber = models.CharField(max_length=10)
    passExpire = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")


    def __str__(self):
        return f"{self.passNumber}"
    

    @staticmethod
    def generate_pass_number():
        last_pass = VehiclePass.objects.order_by('-id').first()
        last_number = int(last_pass.passNumber[-5:]) if last_pass else 0
        new_number = str(last_number + 1).zfill(5)
        return f"VRPSS{new_number}"

    @classmethod
    def create_from_inspection(cls, inspection_report):
        if inspection_report.remarks == "sticker released" and inspection_report.is_approved:
            vehicle = inspection_report.payment_number.registration.vehicle
            
            if not cls.objects.filter(vehicle=vehicle).exists():
                return cls.objects.create(
                    vehicle=vehicle,
                    passNumber=cls.generate_pass_number(),
                    passExpire=now().date() + timedelta(days=365),  # 1-year validity
                    status="active"
                )


class PaymentTransaction(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('void', 'Void')
    ]
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=20, unique=True, null=True)
    cashier = models.ForeignKey(CashierProfile, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    due_date = models.DateTimeField(blank=True, null=True) 
    date_processed = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=75, null=True)

    def save(self, *args, **kwargs):
        # Automatically set due_date when status is pending and due_date is not provided
        if self.status == "pending" and not self.due_date:
            self.due_date = timezone.now() + timedelta(days=7)

        # Check if the object already exists (for updates)
        if self.pk is not None:
            original = PaymentTransaction.objects.get(pk=self.pk)
            if original.status != self.status:  # If status has changed
                self.date_processed = timezone.now().astimezone(pytz.timezone('Asia/Manila'))

        # Save the instance
        super().save(*args, **kwargs)

        # Create an inspection report when the status is "paid" (if not already exists)
        if self.status == "paid":
            from .models import InspectionReport  

            inspection_exists = InspectionReport.objects.filter(payment_number=self).exists()

            if not inspection_exists:  
                InspectionReport.objects.create(
                    payment_number=self, 
                    security=None,
                    remarks="to_be_inspected",  
                    is_approved=False
                )

    def __str__(self):
        return self.receipt_number if self.receipt_number else f"Registration {self.registration.registrationNumber}"

 
class InspectionReport(BaseModel):
    REMARK_CHOICES = [
        ('to be inspected', 'To Be Inspected'),
        ('sticker released', 'Sticker Released'),
        ('application declined', 'Application Declined'),
        ('request refund', 'To Request Refund'),
    ]

    payment_number = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    security = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE, null=True)
    document_inspection_date = models.DateTimeField(auto_now_add=True)
    physical_final_inspection_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=30, choices=REMARK_CHOICES, default='to_be_inspected')
    additional_notes = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Inspection {self.payment_number}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if self.is_approved:
            self.remarks = 'sticker released'

        super().save(*args, **kwargs)
        
        # Check if this is an update and the necessary conditions are met
        if not is_new and self.remarks == "sticker released" and self.is_approved:
            from .models import VehiclePass
            VehiclePass.create_from_inspection(self)

class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('system', 'System'),
        ('user', 'User'),
        ('alert', 'Alert'),
    ]
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="notifications_posted")
    is_read = models.BooleanField(default=False)

class Announcement(BaseModel):
    title = models.CharField(max_length=50)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="announcements_posted")

class SiteVisit(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class LoginActivity(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
