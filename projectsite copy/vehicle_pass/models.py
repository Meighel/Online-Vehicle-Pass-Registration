from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
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
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"  

class SecurityProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badgeNumber = models.CharField(max_length=10)
    job_title = models.CharField(max_length=30)

    def __str__(self):
        return f"Security Personnel: {self.user.firstname} {self.user.lastname} {self.badgeNumber}"  

class CashierProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cashier_id = models.CharField(max_length=15)
    job_title = models.CharField(max_length=40)

    def __str__(self):
        return f"Cashier: {self.user.firstname} {self.user.lastname} {self.cashier_id}"  

class AdminProfile(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=15)

    def __str__(self):
        return f"Admin: {self.user.firstname} {self.user.lastname} ({self.admin_id})"

class Vehicle(BaseModel):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plateNumber = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    chassisNumber = models.CharField(max_length=17)
    OR_Number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.plateNumber}"  
    
    def clean(self):
        if Vehicle.objects.filter(owner=self.owner).count() >= 2:
            raise ValidationError({'owner': 'You can only register up to two vehicles.'})

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.passNumber}"  

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    due_date = models.DateTimeField(blank=True, null=True) 
    date_processed = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.status == "pending" and not self.due_date:
            self.due_date = now() + timedelta(days=7) 

        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_number if self.receipt_number else f"Registration {self.registration.registrationNumber}"
 
class InspectionReport(BaseModel):
    REMARK_CHOICES = [
        ('sticker_released', 'Sticker Released'),
        ('application_declined', 'Application Declined'),
        ('request_refund', 'To Request Refund'),
    ]

    payment_number = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    security = models.ForeignKey(SecurityProfile, on_delete=models.CASCADE)
    inspection_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=30, choices=REMARK_CHOICES, default='sticker_released')
    additional_notes = models.TextField(blank=True, null=True)
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
    posted_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="notifications_posted")
    is_read = models.BooleanField(default=False)

class Announcement(BaseModel):
    title = models.CharField(max_length=50)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="announcements_posted")
