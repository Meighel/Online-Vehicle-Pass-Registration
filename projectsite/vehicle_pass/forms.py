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
        fields = ['corporate_email', 'firstname', 'middlename', 'lastname', 'school_role']

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

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['status', 'remarks', 'initial_approved_by']
        labels = {
            'initial_approved_by': 'Security Personnel'
        }

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

#Personal Information Form 
class VehicleRegistrationStep1Form(forms.Form):
    firstname = forms.CharField(
        max_length=100,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    middlename = forms.CharField(
        max_length=100,
        required=False,
        label='Middle Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your middle name'})
    )
    lastname = forms.CharField(
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
    address = forms.CharField(
        max_length=105,
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Escano St., Brgy Tiniguiban'})
    )  
    contact = forms.CharField(
        label='Contact Number',
        widget=forms.TextInput(attrs={'placeholder': '+6391234567891'})
    )
    corporate_email = forms.EmailField(
        label='Corporate Email',
        widget=forms.EmailInput(attrs={'placeholder': '20228000X@psu.edu.ph'})
    )
    dl_number = forms.CharField(
        max_length=25,
        label="Driver's License Number",
        widget=forms.TextInput(attrs={'placeholder': 'N03-12-123456'})
    )
    
    school_role = forms.ChoiceField(
        choices=[('student', 'Student'), ('faculty & staff', 'Faculty/Staff'), ('university official', 'University Official')],
        label='School Role',
        widget=forms.RadioSelect
    )

    #for employee
    position = forms.CharField(
        max_length=50,
        label="Position",
        widget=forms.TextInput(attrs={'placeholder':'e.g., dean, univeristy librarian, utility, etc.'})
    )
    workplace = forms.ChoiceField(
        choices = UserProfile.WORKPLACE_CHOICES,
        required=False,
        label='Workplace',
        widget=forms.Select(attrs={'placeholder': 'Enter your college or workplace'})
    )

    #for student
    college = forms.ChoiceField(
        choices = UserProfile.COLLEGE_CHOICES,
        required=False,
        label='College',
        widget=forms.Select(attrs={'placeholder': 'Enter your college'})
    )
    program = forms.CharField(
        max_length=100,
        required=False,
        label='Program',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. BS Computer Science'})
    )
    year_level = forms.ChoiceField(
        choices = UserProfile.YEAR_LEVEL_CHOICES,
        required=False,
        label='Year Level',
        widget=forms.Select(attrs={'placeholder': 'Select Year Level'})
    )
    father_name = forms.CharField(
        max_length=100,
        required = False,
        label='Father Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name MI. Surname'})
    )
    father_contact = forms.CharField(
        max_length=100,
        required = False,
        label='Father Contact',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., +6399876543210'})
    )
    father_address = forms.CharField(
        max_length = 150,
        required = False,
        label='Father Address',
        widget=forms.TextInput(attrs={'placeholder': 'Rizal St., Brgy. San Fernando, PPC'})
    )
    mother_name = forms.CharField(
        max_length=100,
        required = False,
        label='Mother Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name MI. Surname'})
    )
    mother_contact = forms.CharField(
        max_length=100,
        required = False,
        label='Mother Contact',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., +6399876543210'})
    )
    mother_address = forms.CharField(
        max_length = 150,
        required = False,
        label='Mother Address',
        widget=forms.TextInput(attrs={'placeholder': 'Rizal St., Brgy. San Fernando, PPC'})
    )
    guardian_name = forms.CharField(
        max_length=100,
        required = False,
        label='Guardian Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name MI. Surname'})
    )
    guardian_contact = forms.CharField(
        max_length=100,
        required = False,
        label='Guardian Contact',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., +6399876543210'})
    )
    guardian_address = forms.CharField(
        max_length = 150,
        required = False,
        label='Guardian Address',
        widget=forms.TextInput(attrs={'placeholder': 'Rizal St., Brgy. San Fernando, PPC'})
    )

class VehicleRegistrationStep2Form(forms.Form):
    #Vehicle Information
    make_model = forms.CharField(
        max_length=100,
        label='Vehicle Model',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Toyota Vios'})
    )
    plate_number = forms.CharField(
        max_length=100,
        label='Plate Number',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ABC-1234'})
    )
    year_model = forms.IntegerField(
        label="Year Model",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 2023'})
    )
    color = forms.CharField(
        max_length=20,
        label='Color',
        widget=forms.TextInput(attrs={'placeholder': 'Enter vehicle color'})
    )
    type = forms.ChoiceField(
        choices= Vehicle.VEHICLE_TYPE,
        label='Vehicle Type',
        widget=forms.Select(attrs={'placeholder': 'Choose type'})
    )
    engine_number = forms.CharField(
        max_length=25,
        label='Engine Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter engine number'})
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

    owner = forms.ChoiceField(
        choices=[('yes', 'Yes, I am the owner of the vehicle'), 
                 ('no', 'No, I am registering on behalf of the owner')],
        label='Are you the owner of this vehicle?',
        widget=forms.RadioSelect()
    )
    owner_firstname = forms.CharField(
        max_length=100,
        required=False,
        label="Owner's First Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's first name"})
    )
    owner_middlename = forms.CharField(
        max_length=100,
        required=False,
        label="Owner's Middle Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's middle name (optional)"})
    )
    owner_lastname = forms.CharField(
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
    relationship_to_owner = forms.CharField(
        max_length=100,
        required=False,
        label='Relationship to Owner',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Father, Mother, etc.'})
    )
    contact_number = forms.CharField(
        max_length=14,
        required=False,
        label="Owner's Contact Number",
        widget=forms.TextInput(attrs={'placeholder': "e.g. +639123456789"})
    )
    address = forms.CharField(
        max_length=100,
        required = False,
        label="Owner's Address",
        widget=forms.TextInput(attrs={'placeholder':'Rizal Street, Brgy. San Fernando, PPC'})
    )

    
    def clean(self):
        cleaned_data = super().clean()
        is_owner = cleaned_data.get("owner") == "yes"

        if not is_owner:
            required_fields = ["owner_firstname", "owner_lastname", "relationship_to_owner", "contact_number", "address"]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required if you're not the owner.")
        return cleaned_data

class VehicleRegistrationStep3Form(forms.Form):
    google_drive_link = forms.URLField(
        label='Google Folder Link',
        widget=forms.URLInput(attrs={'placeholder': 'Paste the link of your Google Drive folder'}) 
    )
    printed_name = forms.CharField(
        max_length = 125,
        label='Printed Name',
        widget = forms.TextInput(attrs={'placeholder': 'First Name MI. Surname Suffix'})
    )
    e_signature = forms.ImageField(
        label='E-signature',
        required=True,
        widget=forms.FileInput(attrs={
            'accept': 'image/*'
        })
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
        fields = '__all__' 