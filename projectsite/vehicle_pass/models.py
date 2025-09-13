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
        ('admin', 'Admin')
        ]
    
    SCHOOL_ROLE_CHOICES = [('student', 'Student'),
                   ('faculty & staff', 'Faculty and Staff'),
                   ('university official', 'University Personnel')
                   ]
    
    COLLEGE_CHOICES = [('CAD'), ('College of Architecture and Design'),
                       ('CAH'), ('College of Arts and Humanities'),
                       ('CBA'), ('College of Business and Accountancy'),
                       ('CCJE'), ('College of Criminal Justice and Education'),
                       ('CoE'), ('College of Engineering'),
                       ('CHTM'), ('College of Hospitality Management and Tourism'),
                       ('CNHS'), ('College of Nursing and Health Sciences'),
                       ('CS'), ('College of Sciences'),
                       ('CTE'), ('College of Teacher Education'),                       
                       ]
    
    OFFICE_CHOICES = [('CAD'), ('College of Architecture and Design'),
                       ('CAH'), ('College of Arts and Humanities'),
                       ('CBA'), ('College of Business and Accountancy'),
                       ('CCJE'), ('College of Criminal Justice and Education'),
                       ('CoE'), ('College of Engineering'),
                       ('CHTM'), ('College of Hospitality Management and Tourism'),
                       ('CNHS'), ('College of Nursing and Health Sciences'),
                       ('CS'), ('College of Sciences'),
                       ('CTE'), ('College of Teacher Education'),                       
                       ]

    # PERSONAL INFORMATION
    corporate_email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=13)
    lastname = models.CharField(max_length=25) 
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=25, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    # FOR STUDENT
    college = models.CharField(max_length=100, choices=COLLEGE_CHOICES ,blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_contact = models.CharField(max_length=13, blank=True, null=True)
    father_address = models.CharField(max_length=150, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_contact =models.CharField(max_length=13, blank=True, null=True)
    mother_address = models.CharField(max_length=150, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=13, blank=True, null=True)
    guardian_address = models.CharField(max_length=150, blank=True, null=True)


    # FOR EMPLOYEE
    position = models.CharField(max_length=50, blank=True, null=True)
    office_or_college = models.CharField(max_length=75, blank=True, null=True)

    #extra fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', null=True)
    school_role = models.CharField(max_length=20, choices=SCHOOL_ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        middle_initial = f"{self.middlename[0]}." if self.middlename else ""
        # Add a space only if middle_initial exists
        return f"{self.firstname} {middle_initial + ' ' if middle_initial else ''}{self.lastname}"

    
    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256$"):  # Prevent double hashing
            self.password = make_password(self.password)  # Hash password before saving
            
        super().save(*args, **kwargs)

        # Create profile based on role if not already existing
        if self.role == 'security' and not hasattr(self, 'securityprofile'):
            SecurityProfile.objects.create(user=self)
        elif self.role == 'admin' and not hasattr(self, 'adminprofile'):
            AdminProfile.objects.create(user=self)


    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Check password

class SecurityProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badgeNumber = models.CharField(max_length=10)
    job_title = models.CharField(max_length=30)

    def __str__(self):
        return f"Security Personnel: {self.user.firstname} {self.user.lastname} {self.badgeNumber}"  

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
    VEHICLE_TYPE = [('motor'), ('Motor'),
                    ('car'), ('Car'),
                    ('van'), ('Van')]
    
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    make_model = models.CharField(max_length=35)
    plate_number = models.CharField(max_length=10, unique=True)
    year_model = models.IntegerField(max_length=4)
    color = models.CharField(max_length=20)
    type = models.CharField(choices=VEHICLE_TYPE, max_length=5)
    engine_number = models.CharField(max_length=25)
    chassis_number = models.CharField(max_length=17)

    def __str__(self):
        return f"{self.plate_number}"  

    def clean(self):
        if Vehicle.objects.filter(applicant=self.applicant).count() >= 2:
            raise ValidationError({'Applicant': 'You can only register up to two vehicles.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Registration(BaseModel):
    STATUS_CHOICES = [
        ('no application', 'No Application'),
        ('application submitted', 'Application Submitted'),
        ('initial approval', 'Waiting for Approval by OIC'),
        ('final approval', 'Waiting for Final Approval by GSO - Director')
        ('approved', 'Approved'),
        ('sticker released', 'Vehicle Pass Sticker Released'),
        ('rejected', 'Rejected')
    ]
    registration_number = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    files = models.URLField(max_length=255)
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='no application')
    remarks = models.TextField(null=True)
    initial_approved_by = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE, null=True, blank=True)
    final_approved_by = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE, null=True, blank=True)
    date_of_filing = models.DateTimeField(auto_now_add=True)
    sticker_released_date = models.DateField(blank=True, null=True)

    # E-signature fields
    e_signature = models.TextField(blank=True, null=True)  # Store signature as base64 data
    printed_name = models.CharField(max_length=255, blank=True, null=True)
    signature_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Registration {self.registration_number} for {self.user.lastname}, {self.user.firstname}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

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
