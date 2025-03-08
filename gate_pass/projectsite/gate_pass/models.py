from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel):
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=25)
    suffix = models.CharField(max_length=5) #if applicable
    dl_number = models.CharField(max_length=15)
    college = models.CharField(max_length=100) #conditional
    program = models.CharField(max_length=100) #conditional
    department = models.CharField(max_length=100) #conditional
    corporate_email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.lastName

class Security(BaseModel):
    badgeNumber = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)
    middleInitial = models.CharField(max_length=5)
    suffix = models.CharField(max_length=5) #if applicable
    corporate_email = models.CharField(max_length=50)
    position = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.lastName}, {self.badgeNumber}"


class Cashier(BaseModel):
    idNumber = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    firstName = models.CharField(max_length=50)
    middleInitial = models.CharField(max_length=5)
    suffix = models.CharField(max_length=5) #if applicable
    corporate_email = models.CharField(max_length=50)

    def __str__(self):
        return self.lastName
    
class Vehicle(BaseModel):
    plateNumber = models.CharField(max_length=10)
    type =models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    chassisNumber = models.CharField(max_length=15)
    OR_Number = models.CharField(max_length=15)

    def __str__(self):
        return self.plateNumber
    
class Pass(BaseModel):
    passNumber = models.CharField(max_length=10)
    passExpire = models.DateField()

    def __str__(self):
        return self.passNumber
    
class Registration(BaseModel):
    applicationNumber = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    files = models.CharField(max_length=250)

    def __str__(self):
        return self.applicationNumber

class Verified(BaseModel):
    passNumber = models.ForeignKey(Pass, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    



    