from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.exceptions import ValidationError
    
class CustomUserManager(BaseUserManager):
    def create_user(self, corporate_email, password=None, **extra_fields):
        if not corporate_email:
            raise ValueError('The email field must be set')
        if not password:
            raise ValueError('Missing Password! Try again.')
        
        extra_fields.setdefault('role', 'user')
    
        user = self.model(corporate_email=self.normalize_email(corporate_email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        profile = UserProfile.objects.create(
            user=user,
            firstname=extra_fields.get('firstname', ''),
            lastname=extra_fields.get('lastname', ''),
            middle_initial = extra_fields.get('middle_initial', ''),
            suffix = extra_fields.get('suffix', ''),
            dl_number = extra_fields.get('dl_number', ''),
            college = extra_fields.get('college', ''),
            program = extra_fields.get('program', ''),
            department = extra_fields.get('department', ''),
            address=extra_fields.get('address', '')
            # Add other common fields as needed.
        )

        role = extra_fields.get('role', 'user')

        if role == 'cashier':
            CashierProfile.objects.create(
                user=profile,
                cashier_id=extra_fields.get('cashier_id', ''),
                job_title=extra_fields.get('job_title', ''),
            )
        elif role == 'security':
            SecurityProfile.objects.create(
                user=profile,
                badgeNumber=extra_fields.get('badgeNumber', ''),
                job_title=extra_fields.get('job_title', ''),
            )
        elif role == 'admin':
            AdminProfile.objects.create(
                user=profile,
                admin_id=extra_fields.get('admin_id', ''),
            )
        
        return user
    
    def create_superuser(self, corporate_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(corporate_email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    role_choices = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('cashier', 'Cashier'),
        ('security', 'Security')
    ]

    corporate_email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=role_choices, default='user')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'corporate_email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.corporate_email} - {self.role}"

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=25)
    firstname = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=25, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    dl_number = models.CharField(max_length=15, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True) 
    program = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class SecurityProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badgeNumber = models.CharField(max_length=10)
    job_title = models.CharField(max_length=30)

    def __str__(self):
        return f"Security Personnel: {self.badgeNumber}"


class CashierProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cashier_id = models.CharField(max_length=15)
    job_title = models.CharField(max_length=40)

    def __str__(self):
        return f"Cashier {self.cashier_id}"

class AdminProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=15)

    def __str__(self):
        return f"Admin {self.admin_id}"
    

class Vehicle(BaseModel):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plateNumber = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    chassisNumber = models.CharField(max_length=15)
    OR_Number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.plateNumber}"
    
    def clean(self):
        if Vehicle.objects.filter(owner=self.owner).count() >= 2:
            raise ValidationError('You can only register up to two vehicles.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Registration(BaseModel): 
    status_choices = [
        ('pending', 'Pending'),
        ('cancelled', 'cancelled'),
        ('for payment', 'For Payment'),
        ('reviewing documents', 'Reviewing Documents'),
        ('for final inspection', 'For Final Inspection'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    registrationNumber = models.CharField(max_length=25)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plate_number = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    files = models.URLField(max_length=250)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return f"{self.registrationNumber}"

    
class VehiclePass(BaseModel):
    status_choices = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked')
    ]
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    passNumber = models.CharField(max_length=10)
    passExpire = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices)

    def __str__(self):
        return f"{self.passNumber}"
    

class PaymentTransaction(BaseModel):
    status_choices = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('void', 'Void')
    ]
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=20, unique=True)
    cashier = models.ForeignKey(CashierProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default="pending")
    date_processed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.receipt_number

class InspectionReport(BaseModel):
    payment_number = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    security = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE)
    inspection_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Inspection {self.payment_number} - {'Approved' if self.is_approved else 'Rejected'}"


class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('system', 'System'),
        ('user', 'User'),
        ('alert', 'Alert'),
    ]
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Announcement(BaseModel):
    title = models.CharField(max_length=50)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="announcements")