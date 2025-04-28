from django import forms
from .models import (UserProfile,
                     PaymentTransaction,
                     Registration,
                     Vehicle,
                     InspectionReport,
                     CashierProfile,
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
        fields = ['status', 'cashier']  # 'cashier' will be auto-filled

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Automatically assign the logged-in cashier to the cashier field
        if 'user' in kwargs:
            user = kwargs['user']
            try:
                # If the user has a related CashierProfile, automatically set it
                cashier_profile = CashierProfile.objects.get(user=user)
                self.fields['cashier'].initial = cashier_profile  # Set the initial value
            except CashierProfile.DoesNotExist:
                # Handle the case where the user is not a cashier
                self.fields['cashier'].initial = None
        # Make the cashier field non-editable
        self.fields['cashier'].widget.attrs['readonly'] = True

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

class VehicleRegistrationStep2Form(forms.Form):
    owner = forms.ChoiceField(choices=[('yes', 'Yes, I am the owner of the vehicle'), 
                                       ('no', 'No, I am registering on behalf of the owner')], 
                              label='Are you the owner of this vehicle?')
    # Owner details if "no" is selected
    owner_first_name = forms.CharField(max_length=100, required=False, label='Owner\'s First Name')
    owner_middle_name = forms.CharField(max_length=100, required=False, label='Owner\'s Middle Name')
    owner_last_name = forms.CharField(max_length=100, required=False, label='Owner\'s Last Name')
    owner_contact_number = forms.CharField(max_length=15, required=False, label='Owner\'s Contact Number')

class VehicleRegistrationStep3Form(forms.Form):
    google_drive_link = forms.URLField(label='Google Folder Link')


class InspectionApprovalForm(forms.ModelForm):
    class Meta:
        model = InspectionReport
        fields = ['remarks', 'additional_notes', 'is_approved']