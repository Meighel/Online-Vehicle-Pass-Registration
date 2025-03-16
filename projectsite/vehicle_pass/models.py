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

        user = self.model(corporate_email = self.normalize_email(corporate_email), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        role = extra_fields.get('role')
        if role == 'user':
            UserProfile.objects.create(
                user=user,
                lastname = extra_fields.get('firstname', ''),
                firstname = extra_fields.get('firstname', ''),
                middle_initial = extra_fields.get('middle_initial', ''),
                suffix = extra_fields.get('suffix', ''),
                dl_number = extra_fields.get('dl_number', ''),
                college = extra_fields.get('college', ''),
                program = extra_fields.get('program', ''),
                department = extra_fields.get('department', ''),
                address = extra_fields.get('address', '')
            )
        elif role =='cashier':
            CashierProfile.objects.create(
                user=user,
                username = extra_fields.get('username', ''),
                lastname = extra_fields.get('lastname', ''),
                firstname = extra_fields.get('firstname', ''),
                middle_initial = extra_fields.get('middle_initial', ''),
                suffix = extra_fields.get('suffix', ''),
                job_title = extra_fields.get('job_title', '')
            )
        elif role =='security':
            SecurityProfile.objects.create(
                user=user,
                username = extra_fields.get('username', ''),
                lastname = extra_fields.get('lastname', ''),
                firstname = extra_fields.get('firstname', ''),
                middle_initial = extra_fields.get('middle_initial', ''),
                suffix = extra_fields.get('suffix', ''),
                job_title = extra_fields.get('job_title', '')
            )
        elif role == 'admin':
            AdminProfile.objects.create(
                user=user,
                username = extra_fields.get('username', ''),
                lastname = extra_fields.get('lastname', ''),
                firstname = extra_fields.get('firstname', ''),
                middle_initial = extra_fields.get('middle_initial', ''),
            )

        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    role_choices = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('cashier', 'Cashier'),
        ('security', 'Security')
    ]

    corporate_email = models.EmailField(max_length=50)
    role = models.CharField(max_length=20, choices=role_choices, default='user')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True
    )

    USERNAME_FIELD = 'corporate_email'
    REQUIRED_FIELDS = ['username']

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
    dl_number = models.CharField(max_length=15)
    college = models.CharField(max_length=100, blank=True, null=True) 
    program = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class SecurityProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    badgeNumber = models.CharField(max_length=10)
    username = models.CharField(max_length=15)
    lastname = models.CharField(max_length=25)
    firstname = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=5)
    suffix = models.CharField(max_length=5)
    job_title = models.CharField(max_length=30)

    def __str__(self):
        return f"Security Personnel {self.lastname}, {self.badgeNumber}"


class CashierProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=15)
    lastname = models.CharField(max_length=25)
    firstname = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=5)
    suffix = models.CharField(max_length=5) #optional
    job_title = models.CharField(max_length=40)

    def __str__(self):
        return f"Cashier {self.firstname} {self.lastname}"

class AdminProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=15)
    lastname = models.CharField(max_length=25)
    firstname = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=5)

    def __str__(self):
        return f"Admin {self.firstname} {self.lastname}"
    

class Vehicle(BaseModel):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plateNumber = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    chassisNumber = models.CharField(max_length=15)
    OR_Number = models.CharField(max_length=15)

    def __str__(self):
        return self.plateNumber
    
    def clean(self):
        if Vehicle.objects.filter(owner=self.owner).count() >= 2:
            raise ValidationError('You can only register up to two vehicles.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Registration(BaseModel): 
    applicationNumber = models.CharField(max_length=25)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    files = models.URLField(max_length=250)

    def __str__(self):
        return self.applicationNumber
    
class RegistrationStatus(BaseModel):
    status_choices = [
        ('pending', 'Pending'),
        ('cancelled', 'cancelled'),
        ('for payment', 'For Payment'),
        ('reviewing documents', 'Reviewing Documents'),
        ('for final inspection', 'For Final Inspection'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=150)
    
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
        return self.passNumber
    

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
    status = models.CharField(max_length=10, choices=status_choices)
    date_processed = models.DateTimeField(auto_now_add=True)


class InspectionReport(BaseModel):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    security = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE)
    inspection_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Inspection {self.registration.applicationNumber} - {'Approved' if self.is_approved else 'Rejected'}"


class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('system', 'System'),
        ('user', 'User'),
        ('alert', 'Alert'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Announcement(BaseModel):
    title = models.CharField(max_length=50)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="announcements")