from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 

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

    USERNAME_FIELD = "corporate_email"
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return f"{self.corporate_email} - {self.role}"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=25, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    dl_number = models.CharField(max_length=15) 
    college = models.CharField(max_length=100, blank=True, null=True) 
    program = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"User {self.firstName} {self.lastName}"
    

class SecurityProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    badgeNumber = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)
    middleInitial = models.CharField(max_length=5)
    suffix = models.CharField(max_length=5) #if applicable
    position = models.CharField(max_length=30)

    def __str__(self):
        return f"Security Personnel {self.lastName}, {self.badgeNumber}"


class CashierProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    idNumber = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)
    middleInitial = models.CharField(max_length=5)
    suffix = models.CharField(max_length=5) #if applicable
    corporate_email = models.CharField(max_length=50)

    def __str__(self):
        return f"Cashier {self.firstName} {self.lastName}"

class AdminProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)

    def __str__(self):
        return f"Admin {self.firstName} {self.lastName}"


    
#start revision here
class Vehicle(BaseModel):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plateNumber = models.CharField(max_length=10)
    type =models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    chassisNumber = models.CharField(max_length=15)
    OR_Number = models.CharField(max_length=15)

    def __str__(self):
        return self.plateNumber
    
class VehiclePass(BaseModel):
    status_choices = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked')
    ]
    passNumber = models.CharField(max_length=10)
    passExpire = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices)

    def __str__(self):
        return self.passNumber
    
class Registration(BaseModel):
    applicationNumber = models.CharField(max_length=25)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    files = models.CharField(max_length=250) #ito yung field for link right?

    def __str__(self):
        return self.applicationNumber
    
class RegistrationStatus(BaseModel):
    status_choices = [
        ('pending', 'Pending'),
        ('for payment', 'For Payment'),
        ('Reviewing Documents', 'Reviewing Documents'),
        ('for final inspection', 'For Final Inspection'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=150)
    
class PaymentStatus(BaseModel):
    status_choices = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('void', 'Void')
    ]
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    cashier = models.ForeignKey(CashierProfile, on_delete=models.CASCADE)
    client = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices)
    date_processed = models.DateTimeField(auto_now_add=True)

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




    



    