# from django import forms
# from .models import (UserProfile,
#                      PaymentTransaction,
#                      Registration,
#                      Vehicle,
#                      InspectionReport,
#                      CashierProfile,
#                      SecurityProfile
# )
# from django.contrib.auth.hashers import make_password
# from django.utils.safestring import mark_safe

# class UserSignupForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
#     password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

#     class Meta:
#         model = UserProfile
#         fields = ['corporate_email', 'firstname', 'middle_name', 'lastname', 'school_role']

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match.")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         # Hash the password manually and save it
#         user.password = make_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = '__all__' 

# class PaymentTransactionForm(forms.ModelForm):
#     class Meta:
#         model = PaymentTransaction
#         fields = ['status', 'cashier']
#         labels = {
#             'cashier': 'Cashier'
#         }

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         if self.user:
#             try:
#                 # Get UserProfile instance
#                 if isinstance(self.user, str):
#                     user_profile = UserProfile.objects.get(id=self.user)
#                 else:
#                     user_profile = self.user
                
#                 # Get cashier profile
#                 cashier_profile = CashierProfile.objects.get(user=user_profile)
                
#                 # Restrict choices to ONLY this cashier - this is the key change
#                 self.fields['cashier'].queryset = CashierProfile.objects.filter(id=cashier_profile.id)
                
#                 # Set the initial value to the current cashier
#                 self.fields['cashier'].initial = cashier_profile
                
#             except CashierProfile.DoesNotExist:
#                 self.fields['cashier'].initial = None

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         # Make absolutely sure the cashier is set
#         if hasattr(self, 'user') and self.user and not instance.cashier:
#             try:
#                 if isinstance(self.user, str):
#                     user_profile = UserProfile.objects.get(id=self.user)
#                 else:
#                     user_profile = self.user
#                 cashier_profile = CashierProfile.objects.get(user=user_profile)
#                 instance.cashier = cashier_profile
#             except (UserProfile.DoesNotExist, CashierProfile.DoesNotExist):
#                 pass
        
#         if commit:
#             instance.save()
#         return instance


# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = ['status', 'remarks', 'document_reviewed_by']
#         labels = {
#             'document_reviewed_by': 'Security Personnel'
#         }

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         if self.user:
#             try:
#                 # Get UserProfile instance
#                 if isinstance(self.user, str):
#                     user_profile = UserProfile.objects.get(id=self.user)
#                 else:
#                     user_profile = self.user
                
#                 security_profile = SecurityProfile.objects.get(user=user_profile)
                
#                 # Restrict choices to ONLY this security profile - this is the key change
#                 self.fields['document_reviewed_by'].queryset = SecurityProfile.objects.filter(id=security_profile.id)
                
#                 # Set the initial value
#                 self.fields['document_reviewed_by'].initial = security_profile
                
#             except SecurityProfile.DoesNotExist:
#                 self.fields['document_reviewed_by'].initial = None

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         # Make absolutely sure the reviewer is set
#         if hasattr(self, 'user') and self.user and not instance.document_reviewed_by:
#             try:
#                 if isinstance(self.user, str):
#                     user_profile = UserProfile.objects.get(id=self.user)
#                 else:
#                     user_profile = self.user
#                 security_profile = SecurityProfile.objects.get(user=user_profile)
#                 instance.document_reviewed_by = security_profile
#             except (UserProfile.DoesNotExist, SecurityProfile.DoesNotExist):
#                 pass
        
#         if commit:
#             instance.save()
#         return instance

  
# class VehicleRegistrationStep1Form(forms.Form):
#     first_name = forms.CharField(
#         max_length=100,
#         label='First Name',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
#     )
#     middle_name = forms.CharField(
#         max_length=100,
#         required=False,
#         label='Middle Name',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter your middle name'})
#     )
#     last_name = forms.CharField(
#         max_length=100,
#         label='Last Name',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
#     )
#     suffix = forms.CharField(
#         max_length=5,
#         required=False,
#         label='Suffix',
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. Jr'})
#     )  
#     corporate_email = forms.EmailField(
#         label='Corporate Email',
#         widget=forms.EmailInput(attrs={'placeholder': '20228000X@psu.edu.ph'})
#     )
#     address = forms.CharField(
#         max_length=105,
#         label='Address',
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. Escano St., Brgy Tiniguiban'})
#     )
#     role = forms.ChoiceField(
#         choices=[('student', 'Student'), ('faculty', 'Faculty'), ('university personnel', 'University Personnel')],
#         label='School Role',
#         widget=forms.Select(attrs={'placeholder': 'Select your role'})
#     )
#     department_or_workplace = forms.CharField(
#         max_length=100,
#         required=False,
#         label='Department/Workplace',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter your college or workplace'})
#     )
#     college = forms.CharField(
#         max_length=100,
#         required=False,
#         label='College',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter your college'})
#     )
#     program = forms.CharField(
#         max_length=100,
#         required=False,
#         label='Program',
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. BS Computer Science'})
#     )
#     driver_license_number = forms.CharField(
#         max_length=100,
#         label="Driver's License Number",
#         widget=forms.TextInput(attrs={'placeholder': 'N03-12-123456'})
#     )
#     vehicle_type = forms.ChoiceField(
#         choices=[('car', 'Car'), ('motorcycle', 'Motorcycle')],
#         label='Vehicle Type',
#         widget=forms.RadioSelect(attrs={'placeholder': 'Choose type'})
#     )
#     vehicle_color = forms.CharField(
#         max_length=100,
#         label='Vehicle Color',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter vehicle color'})
#     )
#     model = forms.CharField(
#         max_length=100,
#         label='Vehicle Model',
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. Toyota Vios'})
#     )
#     plate_number = forms.CharField(
#         max_length=100,
#         label='Plate Number',
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. ABC-1234'})
#     )
#     chassis_number = forms.CharField(
#         max_length=100,
#         label='Chassis Number',
#         widget=forms.TextInput(attrs={'placeholder': 'Enter chassis number'})
#     )
#     or_number = forms.CharField(
#         max_length=100,
#         label='OR Number',
#         widget=forms.TextInput(attrs={'placeholder': 'Official Receipt Number'})
#     )
#     cr_number = forms.CharField(
#         max_length=100,
#         label='CR Number',
#         widget=forms.TextInput(attrs={'placeholder': 'Certificate of Registration Number'})
#     )

# class VehicleRegistrationStep2Form(forms.Form):
#     owner = forms.ChoiceField(
#         choices=[('yes', 'Yes, I am the owner of the vehicle'), 
#                  ('no', 'No, I am registering on behalf of the owner')],
#         label='Are you the owner of this vehicle?',
#         widget=forms.RadioSelect()
#     )
#     relationship_to_owner = forms.CharField(
#         max_length=100,
#         required=False,
#         label='Relationship to Owner',
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. Father, Mother, etc.'})
#     )
#     owner_first_name = forms.CharField(
#         max_length=100,
#         required=False,
#         label="Owner's First Name",
#         widget=forms.TextInput(attrs={'placeholder': "Enter owner's first name"})
#     )
#     owner_middle_name = forms.CharField(
#         max_length=100,
#         required=False,
#         label="Owner's Middle Name",
#         widget=forms.TextInput(attrs={'placeholder': "Enter owner's middle name (optional)"})
#     )
#     owner_last_name = forms.CharField(
#         max_length=100,
#         label="Owner's Last Name",
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': "Enter owner's last name"})
#     )
#     owner_suffix = forms.CharField(
#         max_length=5,
#         required=False,
#         label="Owner's Suffix",
#         widget=forms.TextInput(attrs={'placeholder': "e.g. Jr"})
#     )
#     owner_contact_number = forms.CharField(
#         max_length=15,
#         required=False,
#         label="Owner's Contact Number",
#         widget=forms.TextInput(attrs={'placeholder': "e.g. 09123456789"})
#     )
    
#     def clean(self):
#         cleaned_data = super().clean()
#         is_owner = cleaned_data.get("owner") == "yes"

#         if not is_owner:
#             required_fields = ["owner_first_name", "owner_last_name", "relationship_to_owner", "owner_contact_number"]
#             for field in required_fields:
#                 if not cleaned_data.get(field):
#                     self.add_error(field, "This field is required if you're not the owner.")
#         return cleaned_data

# class VehicleRegistrationStep3Form(forms.Form):
#     google_drive_link = forms.URLField(
#         label='Google Folder Link',
#         widget=forms.URLInput(attrs={'placeholder': 'Paste the link of your Google Drive folder'}) 
#     )

# class InspectionApprovalForm(forms.ModelForm):
#     class Meta:
#         model = InspectionReport
#         fields = ['remarks', 'additional_notes', 'is_approved']

# class PasswordUpdateForm(forms.Form):
#     old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password')
#     new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')
    
#     def clean(self):
#         cleaned_data = super().clean()
#         if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
#             raise forms.ValidationError("New passwords and confirmation do not match.")
        
# class VehicleForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = '__all__'  # Changed from 'exclude' to 'fields' as the original had an incorrect usage

# class FinalDateInspectionForm(forms.ModelForm):
#     class Meta:
#         model = InspectionReport
#         fields = ['physical_final_inspection_date', ]
#         widgets = {
#             'physical_final_inspection_date': forms.DateInput(attrs={
#                 'type': 'date', 
#                 'class': 'form-control',
#             }),
#         }


from django import forms
from .models import (UserProfile,
                     Registration,
                     Vehicle,
                     SecurityProfile
)
from django.contrib.auth.hashers import make_password
from django.utils.safestring import mark_safe

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = UserProfile
        fields = ['corporate_email', 'firstname', 'middle_name', 'lastname', 'school_role']

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


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['status', 'remarks']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            try:
                # Get UserProfile instance
                if isinstance(self.user, str):
                    user_profile = UserProfile.objects.get(id=self.user)
                else:
                    user_profile = self.user
                
                security_profile = SecurityProfile.objects.get(user=user_profile)
                
                # Restrict choices to ONLY this security profile - this is the key change
                self.fields['document_reviewed_by'].queryset = SecurityProfile.objects.filter(id=security_profile.id)
                
                # Set the initial value
                self.fields['document_reviewed_by'].initial = security_profile
                
            except SecurityProfile.DoesNotExist:
                self.fields['document_reviewed_by'].initial = None

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Make absolutely sure the reviewer is set
        if hasattr(self, 'user') and self.user and not instance.document_reviewed_by:
            try:
                if isinstance(self.user, str):
                    user_profile = UserProfile.objects.get(id=self.user)
                else:
                    user_profile = self.user
                security_profile = SecurityProfile.objects.get(user=user_profile)
                instance.document_reviewed_by = security_profile
            except (UserProfile.DoesNotExist, SecurityProfile.DoesNotExist):
                pass
        
        if commit:
            instance.save()
        return instance

  
class VehicleRegistrationStep1Form(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    middle_name = forms.CharField(
        max_length=100,
        required=False,
        label='Middle Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your middle name'})
    )
    last_name = forms.CharField(
        max_length=100,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    suffix = forms.CharField(
        max_length=5,
        required=False,
        label='Suffix',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Jr'})
    )  
    corporate_email = forms.EmailField(
        label='Corporate Email',
        widget=forms.EmailInput(attrs={'placeholder': '20228000X@psu.edu.ph'})
    )
    address = forms.CharField(
        max_length=105,
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Escano St., Brgy Tiniguiban'})
    )
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('faculty', 'Faculty'), ('university personnel', 'University Personnel')],
        label='School Role',
        widget=forms.Select(attrs={'placeholder': 'Select your role'})
    )
    department_or_workplace = forms.CharField(
        max_length=100,
        required=False,
        label='Department/Workplace',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your college or workplace'})
    )
    college = forms.CharField(
        max_length=100,
        required=False,
        label='College',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your college'})
    )
    program = forms.CharField(
        max_length=100,
        required=False,
        label='Program',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. BS Computer Science'})
    )
    driver_license_number = forms.CharField(
        max_length=100,
        label="Driver's License Number",
        widget=forms.TextInput(attrs={'placeholder': 'N03-12-123456'})
    )
    vehicle_type = forms.ChoiceField(
        choices=[('car', 'Car'), ('motorcycle', 'Motorcycle')],
        label='Vehicle Type',
        widget=forms.RadioSelect(attrs={'placeholder': 'Choose type'})
    )
    vehicle_color = forms.CharField(
        max_length=100,
        label='Vehicle Color',
        widget=forms.TextInput(attrs={'placeholder': 'Enter vehicle color'})
    )
    model = forms.CharField(
        max_length=100,
        label='Vehicle Model',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Toyota Vios'})
    )
    plate_number = forms.CharField(
        max_length=100,
        label='Plate Number',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ABC-1234'})
    )
    chassis_number = forms.CharField(
        max_length=100,
        label='Chassis Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter chassis number'})
    )
    or_number = forms.CharField(
        max_length=100,
        label='OR Number',
        widget=forms.TextInput(attrs={'placeholder': 'Official Receipt Number'})
    )
    cr_number = forms.CharField(
        max_length=100,
        label='CR Number',
        widget=forms.TextInput(attrs={'placeholder': 'Certificate of Registration Number'})
    )

class VehicleRegistrationStep2Form(forms.Form):
    owner = forms.ChoiceField(
        choices=[('yes', 'Yes, I am the owner of the vehicle'), 
                 ('no', 'No, I am registering on behalf of the owner')],
        label='Are you the owner of this vehicle?',
        widget=forms.RadioSelect()
    )
    relationship_to_owner = forms.CharField(
        max_length=100,
        required=False,
        label='Relationship to Owner',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Father, Mother, etc.'})
    )
    owner_first_name = forms.CharField(
        max_length=100,
        required=False,
        label="Owner's First Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's first name"})
    )
    owner_middle_name = forms.CharField(
        max_length=100,
        required=False,
        label="Owner's Middle Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's middle name (optional)"})
    )
    owner_last_name = forms.CharField(
        max_length=100,
        label="Owner's Last Name",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's last name"})
    )
    owner_suffix = forms.CharField(
        max_length=5,
        required=False,
        label="Owner's Suffix",
        widget=forms.TextInput(attrs={'placeholder': "e.g. Jr"})
    )
    owner_contact_number = forms.CharField(
        max_length=15,
        required=False,
        label="Owner's Contact Number",
        widget=forms.TextInput(attrs={'placeholder': "e.g. 09123456789"})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        is_owner = cleaned_data.get("owner") == "yes"

        if not is_owner:
            required_fields = ["owner_first_name", "owner_last_name", "relationship_to_owner", "owner_contact_number"]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required if you're not the owner.")
        return cleaned_data

class VehicleRegistrationStep3Form(forms.Form):
    google_drive_link = forms.URLField(
        label='Google Folder Link',
        widget=forms.URLInput(attrs={'placeholder': 'Paste the link of your Google Drive folder'}) 
    )

class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("New passwords and confirmation do not match.")
        
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'  # Changed from 'exclude' to 'fields' as the original had an incorrect usage