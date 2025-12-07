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
                           ('university official', 'University Official')
    ]
    
    COLLEGE_CHOICES = [('CAD', 'College of Architecture and Design'),
                       ('CAH', 'College of Arts and Humanities'),
                       ('CBA', 'College of Business and Accountancy'),
                       ('CCJE', 'College of Criminal Justice and Education'),
                       ('CoE', 'College of Engineering'),
                       ('CHTM', 'College of Hospitality Management and Tourism'),
                       ('CNHS', 'College of Nursing and Health Sciences'),
                       ('CS', 'College of Sciences'),
                       ('CTE', 'College of Teacher Education'),
    ]

    YEAR_LEVEL_CHOICES = [('first year', 'First Year'),
                          ('second year', 'Second Year'),
                          ('third year', 'Third Year'),
                          ('fourth year', 'Fourth year'),
                          ('fifth year', 'Fifth Year')
    ]

    OFFICE_CHOICES = [
        ('university president', 'University President'),
        ('university president coa', 'University President COA'),
        ('office of the university secretary', 'Office of the University Secretary'),
        ('legal office', 'Legal Office (Data Privacy Office)'),
        ('planning and development office', 'Planning and Development Office'),
        ('office of the internal audit services', 'Office of the Internal Audit Services (QMS)'),
        ('public information office', 'Public Information Office'),
        ('alumni affairs office', 'Alumni Affairs Office'),
        ('academic council', 'Academic Council'),
        ('administrative council', 'Administrative Council'),
        ('research and extension council', 'Research and Extension Council'),
        ('management committee', 'Management Committee'),
        ('university ethics committee', 'University Ethics Committee'),
        ('gender and development office', 'Gender and Development Office'),
        ('international affairs and linkages office', 'International Affairs and Linkages Office'),
        ('office of the vice president for finance and administration', 'Office of the Vice President for Finance and Administration'),
        ('bids and awards committee', 'Bids and Awards Committee'),
        ('administrative management office', 'Administrative Management Office'),
        ('records archives management office', 'Records Archives Management Office'),
        ('human resource management office', 'Human Resource Management Office'),
        ('faculty and staff development unit', 'Faculty and Staff Development Unit'),
        ('health services office', 'Health Services Office'),
        ('management information system information office', 'Management Information System Information Office'),
        ('security office', 'Security Office'),
        ('supply and property management office', 'Supply and Property Management Office'),
        ('disaster risk reduction and management office', 'Disaster Risk Reduction and Management Office'),
        ('project management office', 'Project Management Office'),
        ('general services office', 'General Services Office'),
        ('utility and environmental management office', 'Utility and Environmental Management Office'),
        ('motorpool office', 'Motorpool Office'),
        ('finance management service offices (cfo)', 'Finance Management Service Offices (CFO)'),
        ('accounting office', 'Accounting Office'),
        ('processing unit', 'Processing Unit'),
        ('student accounts & assessment', 'Student Accounts & Assessment'),
        ('financial reporting', 'Financial Reporting'),
        ('budget office', 'Budget Office'),
        ('production services/income generating projects office', 'Production Services/Income Generating Projects Office'),
        ('production', 'Production'),
        ('sifma', 'SIFMA'),
        ('university bookstore', 'University Bookstore'),
        ('auxiliary services - canteen', 'Auxiliary Services - Canteen'),
        ('auxiliary services - hostel', 'Auxiliary Services - Hostel'),
        ('auxiliary services - dormitory', 'Auxiliary Services - Dormitory'),
        ('university printing press', 'University Printing Press'),
        ('procurement office', 'Procurement Office'),
        ('cashiers office', 'Cashier’s Office'),
        ('office of the vice president for research, development and extension', 'Office of the Vice President for Research, Development and Extension'),
        ('university research office', 'University Research Office'),
        ('university extension service office', 'University Extension Service Office'),
        ('intellectual property and technology transfer office', 'Intellectual Property and Technology Transfer Office'),
        ('palawan studies center', 'Palawan Studies Center'),
        ('center for strategy policy and governance', 'Center for Strategy Policy and Governance'),
        ('panrehiyong iv-b sentro ng wikang pilipino', 'Panrehiyong IV-B Sentro ng Wikang Pilipino'),
        ('marine science research center', 'Marine Science Research Center'),
        ('palawan international technology business incubator & startup hub office', 'Palawan International Technology Business Incubator & Startup Hub Office'),
        ('office of the vice president for academic affairs', 'Office of the Vice President for Academic Affairs'),
        ('office of the eteeap', 'Office of the ETEEAP'),
        ('office of the university registrar', 'Office of the University Registrar'),
        ('university quality assurance center', 'University Quality Assurance Center'),
        ('office of the university sports', 'Office of the University Sports'),
        ('office of the curriculum & instructional materials development', 'Office of the Curriculum & Instructional Materials Development'),
        ('office of the student affairs and services', 'Office of the Student Affairs and Services'),
        ('social and cultural affairs (psu band, psu dance troupe, psu singers)', 'Social and Cultural Affairs (PSU Band, PSU Dance Troupe, PSU Singers)'),
        ('office of the university library', 'Office of the University Library'),
        ('psu museum', 'PSU Museum'),
    ]

    WORKPLACE_CHOICES = OFFICE_CHOICES + COLLEGE_CHOICES    

    # PERSONAL INFORMATION
    corporate_email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=14)
    lastname = models.CharField(max_length=25) 
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=25, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    dl_number = models.CharField(max_length=25)

    # FOR STUDENT
    college = models.CharField(max_length=100, choices=COLLEGE_CHOICES ,blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    year_level = models.CharField(max_length=40, choices=YEAR_LEVEL_CHOICES, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_contact = models.CharField(max_length=14, blank=True, null=True)
    father_address = models.CharField(max_length=150, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_contact =models.CharField(max_length=14, blank=True, null=True)
    mother_address = models.CharField(max_length=150, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=14, blank=True, null=True)
    guardian_address = models.CharField(max_length=150, blank=True, null=True)


    # FOR EMPLOYEE
    position = models.CharField(max_length=50, blank=True, null=True)
    workplace = models.CharField(max_length=150, choices=WORKPLACE_CHOICES, blank=True, null=True)

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
    SECURITY_LEVEL_CHOICES = [('guard', 'Security Guard/Personnel'),
                      ('oic', 'Security OIC'),
                      ('gso director', 'GSO - Director')]

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    badgeNumber = models.CharField(max_length=10)
    job_title = models.CharField(max_length=30)

    level = models.CharField(max_length=20, choices=SECURITY_LEVEL_CHOICES, default='guard')

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} ({self.get_level_display()})" 

class AdminProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    admin_id = models.IntegerField(primary_key=True)

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
    VEHICLE_TYPE = [('motor', 'Motor'),
                    ('car', 'Car'),
                    ('van', 'Van')]
    
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    make_model = models.CharField(max_length=35)
    plate_number = models.CharField(max_length=10, unique=True)
    year_model = models.IntegerField()
    color = models.CharField(max_length=20)
    type = models.CharField(choices=VEHICLE_TYPE, max_length=5)
    engine_number = models.CharField(max_length=25)
    chassis_number = models.CharField(max_length=17)
    or_number = models.CharField(max_length=25)
    cr_number = models.CharField(max_length=25)

    # Only relevant if not the owner
    owner_firstname = models.CharField(max_length=45, null=True, blank=True)
    owner_middlename = models.CharField(max_length=45, null=True, blank=True)
    owner_lastname = models.CharField(max_length=45, null=True, blank=True)
    owner_suffix = models.CharField(max_length=5, null=True, blank=True)
    relationship_to_owner = models.CharField(max_length=15, null=True, blank=True)
    contact_number = models.CharField(max_length=14, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    @property
    def is_owner(self):
        return not any([
            self.owner_firstname,
            self.owner_middlename,
            self.owner_lastname,
            self.owner_suffix,
            self.relationship_to_owner,
            self.contact_number,
            self.address
        ])

    def __str__(self):
        return f"{self.plate_number}"  

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
            ('no application', 'No Application'),
            # When created, it waits for OIC:
            ('application submitted', 'Pending Initial Approval (OIC)'), 
            
            # When OIC approves, it waits for Director:
            ('initial approval', 'Initial Approved (Waiting for GSO Director)'), 
            
            # When Director approves, it is Ready for Release:
            ('final approval', 'Final Approved (Ready for Sticker)'), 
            
            ('approved', 'Approved'),
            ('sticker released', 'Vehicle Pass Sticker Released'),
            ('rejected', 'Rejected')
        ]
    registration_number = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    files = models.URLField(max_length=255)
    status = models.CharField(max_length=85, choices=STATUS_CHOICES, default='no application')
    remarks = models.TextField(null=True)
    initial_approved_by = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE, related_name='initial_approval', null=True, blank=True)
    final_approved_by = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE, related_name='final_approval', null=True, blank=True)
    date_of_filing = models.DateTimeField(auto_now_add=True)
    sticker_released_date = models.DateField(blank=True, null=True)

    # E-signature fields
    e_signature = models.ImageField(upload_to='signature/')
    printed_name = models.CharField(max_length=125)
    signature_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Registration {self.registration_number} for {self.user.lastname}, {self.user.firstname}"

    def save(self, *args, **kwargs):
        # Check if this is an update and status changed
        if self.pk:
            try:
                old_instance = Registration.objects.get(pk=self.pk)
                status_changed = old_instance.status != self.status
            except Registration.DoesNotExist:
                status_changed = False
        else:
            status_changed = True
            
        super().save(*args, **kwargs)
        
        # If status changed, create notification immediately
        if status_changed:
            self._create_status_notification()
    
    def _create_status_notification(self):
        """Create notification when status changes"""
        from .notification_utils import create_registration_notification
        create_registration_notification(self)

class VehiclePass(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked')
    ]
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    pass_number = models.CharField(max_length=20)
    pass_expire = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.pass_number}"
    
    @staticmethod
    def generate_pass_number(user_school_role):
        """
        Generate pass number based on user's school role:
        - Student: STUDENT001 (limit: 2500)
        - University Official: UNIVERSITY OFFICIALS001 (limit: 500)  
        - Faculty & Staff: FACULTY AND STAFF0001 (limit: 1000)
        """
        
        if user_school_role == 'student':
            # Get last student pass number
            student_passes = VehiclePass.objects.filter(
                pass_number__startswith='STUDENT'
            ).order_by('-id')
            
            if student_passes.exists():
                last_pass = student_passes.first()
                # Extract number from format like "STUDENT001"
                last_number = int(last_pass.pass_number.replace('STUDENT', ''))
                new_number = last_number + 1
            else:
                new_number = 1
                
            if new_number > 2500:
                raise ValueError("Student pass limit (2500) exceeded")
                
            return f"STUDENTS {str(new_number).zfill(3)}"
            
        elif user_school_role == 'university official':
            # Get last university official pass number
            official_passes = VehiclePass.objects.filter(
                pass_number__startswith='UNIVERSITY OFFICIALS'
            ).order_by('-id')
            
            if official_passes.exists():
                last_pass = official_passes.first()
                # Extract number from format like "UNIVERSITY OFFICIALS001"
                last_number = int(last_pass.pass_number.replace('UNIVERSITY OFFICIALS', ''))
                new_number = last_number + 1
            else:
                new_number = 1
                
            if new_number > 500:
                raise ValueError("University Officials pass limit (500) exceeded")
                
            return f"UNIVERSITY OFFICIALS {str(new_number).zfill(3)}"
            
        elif user_school_role == 'faculty & staff':
            # Get last faculty & staff pass number
            faculty_passes = VehiclePass.objects.filter(
                pass_number__startswith='FACULTY AND STAFF'
            ).order_by('-id')
            
            if faculty_passes.exists():
                last_pass = faculty_passes.first()
                # Extract number from format like "FACULTY AND STAFF0001"
                last_number = int(last_pass.pass_number.replace('FACULTY AND STAFF', ''))
                new_number = last_number + 1
            else:
                new_number = 1
                
            if new_number > 1000:
                raise ValueError("Faculty and Staff pass limit (1000) exceeded")
                
            return f"FACULTY AND STAFF {str(new_number).zfill(4)}"
        else:
            # Fallback to original format for unknown roles
            last_pass = VehiclePass.objects.order_by('-id').first()
            last_number = int(last_pass.pass_number[-5:]) if last_pass else 0
            new_number = str(last_number + 1).zfill(5)
            return f"VRPSS{new_number}"

    @classmethod
    def create_from_registration(cls, registration):
        """
        Create vehicle pass from registration when status is 'sticker released'
        """
        if registration.status == "sticker released":
            vehicle = registration.vehicle
            user_school_role = registration.user.school_role
            
            # Check if vehicle pass already exists for this vehicle
            if not cls.objects.filter(vehicle=vehicle).exists():
                vehicle_pass = cls.objects.create(
                    vehicle=vehicle,
                    pass_number=cls.generate_pass_number(user_school_role),
                    pass_expire=now().date() + timedelta(days=365),  # 1-year validity
                    status="active"
                )
                
                # Update registration sticker_released_date if not already set
                if not registration.sticker_released_date:
                    registration.sticker_released_date = now().date()
                    registration.save(update_fields=['sticker_released_date'])
                
                return vehicle_pass
            else:
                # If vehicle pass already exists, just return the existing one
                return cls.objects.get(vehicle=vehicle)
        else:
            raise ValueError(f"Cannot create vehicle pass. Registration status is '{registration.status}', expected 'sticker released'")

    @classmethod
    def create_vehicle_pass(cls, vehicle, user_school_role):
        """
        Direct method to create vehicle pass with user school role
        """
        if not cls.objects.filter(vehicle=vehicle).exists():
            return cls.objects.create(
                vehicle=vehicle,
                pass_number=cls.generate_pass_number(user_school_role),
                pass_expire=now().date() + timedelta(days=365),
                status="active"
            )
        else:
            raise ValueError("Vehicle pass already exists for this vehicle")
        
class NotificationQueue(BaseModel):
    """This is for the queue of pending notifications"""
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    message = models.TextField()
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()

    #Processing Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)

    #Timing
    scheduled_for = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)

    #Metadata
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)

class Notification(BaseModel):
    """In-app notifications for users"""
    NOTIFICATION_TYPES = [
        ('application update', 'Application Update'),
        ('system announcement', 'System Announcement'),
        ('reminder', 'Reminder'),
    ]
    
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='application update')
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_email_sent = models.BooleanField(default=False)
    
    # Action URL for clickable notifications
    action_url = models.CharField(max_length=255, blank=True, null=True)
    
    # Expiry for temporary notifications
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

class EmailTemplate(BaseModel):
    """Email templates for different notification types"""
    template_name = models.CharField(max_length=100, unique=True)
    subject_template = models.CharField(max_length=255)
    body_template = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def render_subject(self, context):
        return self.subject_template.format(**context)
    
    def render_body(self, context):
        return self.body_template.format(**context)

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
