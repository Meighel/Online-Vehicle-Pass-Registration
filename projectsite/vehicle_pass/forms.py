from django import forms
from .models import (UserProfile,
                     PaymentTransaction,
                     Registration,
                     Vehicle,
                     InspectionReport,
)
from django.contrib.auth.hashers import make_password

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = UserProfile
        fields = ['corporate_email', 'firstname', 'lastname']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password manually and save it
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__' 


class PaymentTransactionForm(forms.ModelForm):
    class Meta:
        model = PaymentTransaction
        fields = ['status']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['status']
        

class VehicleRegistrationStep1Form(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name')
    middle_name = forms.CharField(max_length=100, required=False, label='Middle Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    corporate_email = forms.EmailField(label='Corporate Email')
    role = forms.ChoiceField(choices=[('student', 'Student'), ('faculty', 'Faculty')], label='School Role')
    driver_license_number = forms.CharField(max_length=100, label="Driver's License Number")
    vehicle_type = forms.ChoiceField(choices=[('car', 'Car'), ('motorbike', 'Motorbike')], label='Vehicle Type')
    model = forms.CharField(max_length=100, label='Vehicle Model')
    plate_number = forms.CharField(max_length=100, label='Plate Number')
    chassis_number = forms.CharField(max_length=100, label='Chassis Number')
    or_number = forms.CharField(max_length=100, label='OR Number')
    cr_number = forms.CharField(max_length=100, label='CR Number')
    
    def save(self, commit=True):
        # Get or create user profile
        user_data = {
            'firstname': self.cleaned_data['first_name'],
            'lastname': self.cleaned_data['last_name'],
            'middle_name': self.cleaned_data['middle_name'],
            'dl_number': self.cleaned_data['driver_license_number']
        }
        
        try:
            user = UserProfile.objects.get(corporate_email=self.cleaned_data['corporate_email'])
            # Update existing user with form data
            for key, value in user_data.items():
                setattr(user, key, value)
            if commit:
                user.save()
        except UserProfile.DoesNotExist:
            return None, None
        
        # Create vehicle object
        vehicle = Vehicle(
            owner=user,
            plateNumber=self.cleaned_data['plate_number'],
            type=self.cleaned_data['vehicle_type'],
            model=self.cleaned_data['model'],
            chassisNumber=self.cleaned_data['chassis_number'],
            OR_Number=self.cleaned_data['or_number']
            # Note: CR_Number is not in your model, but in your form
        )
        
        if commit:
            vehicle.save()
            
        # Store data to be used in subsequent steps
        self.user = user
        self.vehicle = vehicle
        
        return user, vehicle


class VehicleRegistrationStep2Form(forms.Form):
    owner = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], label="Are you the owner of this vehicle?")
    owner_first_name = forms.CharField(max_length=100, required=False, label="Owner's First Name")
    owner_middle_name = forms.CharField(max_length=100, required=False, label="Owner's Middle Name")
    owner_last_name = forms.CharField(max_length=100, required=False, label="Owner's Last Name")
    owner_contact_number = forms.CharField(max_length=15, required=False, label="Owner's Contact Number")
    
    def save(self, user=None, vehicle=None, commit=True):
        # If the form indicates the user is not the owner, we could store this information
        # Perhaps in a custom field or related model (not currently in your models.py)
        # For now, we'll just return the existing vehicle
        
        if self.cleaned_data['owner'] == 'no':
            # You might want to create an owner info model or add fields to Vehicle
            # For now, we're just collecting this data but not using it
            # You could extend your models to store this information
            pass
            
        return vehicle


class VehicleRegistrationStep3Form(forms.Form):
    google_drive_link = forms.URLField(label='Google Folder Link')
    
    def save(self, user=None, vehicle=None, commit=True):
        # Create registration entry
        registration = Registration(
            user=user,
            vehicle=vehicle,
            files=self.cleaned_data['google_drive_link'],
            status='pending'  # Default status from your model
        )
        
        if commit:
            registration.save()
            
        return registration


class InspectionApprovalForm(forms.ModelForm):
    class Meta:
        model = InspectionReport
        fields = ['remarks', 'additional_notes', 'is_approved']