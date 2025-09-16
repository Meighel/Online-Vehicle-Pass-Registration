from django import forms
from .models import (UserProfile,
                     Registration,
                     Vehicle,
                     SecurityProfile,
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
    
   #Personal Information 
    lastname = forms.CharField(
        max_length=100,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
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
    dl_number = forms.CharField(
        max_length=20,
        label='Driver\'s License Number',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. NO3-12-123456'})
    )
    contact = forms.CharField(
        max_length=15,
        label='Contact',
        widget=forms.NumberInput(attrs={'placeholder': '09382129173'})
    )
    corporate_email = forms.EmailField(
        label='Corporate Email',
        widget=forms.EmailInput(attrs={'placeholder': '20228000X@psu.edu.ph'})
    )
    school_role = forms.ChoiceField(
        choices=[('student', 'Student'), ('faculty', 'Faculty'), ('university personnel', 'University Personnel')],
        label='School Role',
        widget=forms.Select(attrs={'placeholder': 'Select your role'})
    )
    
    #For Employees
    position = forms.CharField(
        max_length=30,
        required=False,
        label='Position',
        widget=forms.TextInput(attrs={'placeholder': 'For employees only'})
    )
    workplace = forms.ChoiceField(
        choices=UserProfile.WORKPLACE_CHOICES,
        required=False,
        label='Workplace/College',
        widget=forms.Select()
    )
    
    year_level = forms.ChoiceField(
        choices=UserProfile.YEAR_LEVEL_CHOICES,
        required=False,
        label='Year Level',
        widget=forms.Select()
    )
    #For Student
    college = forms.ChoiceField(
        choices=UserProfile.COLLEGE_CHOICES,
        required=False,
        label='College',
        widget=forms.Select()
    )
    program = forms.CharField(
        max_length=100,
        required=False,
        label='Program',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. BS Computer Science'})
    )
    father_name = forms.CharField(
        max_length=100,
        required=False,
        label="Father's Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter father's full name"})
    )
    father_contact = forms.CharField(
        max_length=13,
        required=False,
        label="Father's Contact",
        widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'})
    )
    father_address = forms.CharField(
        max_length=150,
        required=False,
        label="Father's Address",
        widget=forms.TextInput(attrs={'placeholder': "Enter father's address"})
    )

    mother_name = forms.CharField(
        max_length=100,
        required=False,
        label="Mother's Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter mother's full name"})
    )
    mother_contact = forms.CharField(
        max_length=13,
        required=False,
        label="Mother's Contact",
        widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'})
    )
    mother_address = forms.CharField(
        max_length=150,
        required=False,
        label="Mother's Address",
        widget=forms.TextInput(attrs={'placeholder': "Enter mother's address"})
    )

    guardian_name = forms.CharField(
        max_length=100,
        required=False,
        label="Guardian's Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter guardian's full name"})
    )
    guardian_contact = forms.CharField(
        max_length=13,
        required=False,
        label="Guardian's Contact",
        widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'})
    )
    guardian_address = forms.CharField(
        max_length=150,
        required=False,
        label="Guardian's Address",
        widget=forms.TextInput(attrs={'placeholder': "Enter guardian's address"})
    )

class VehicleRegistrationStep2Form(forms.Form):
    # Vehicle Information
    make_model = forms.CharField(
        max_length=35,
        label="Vehicle Make and Model",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Toyota Vios, Honda Click'})
    )
    plate_number = forms.CharField(
        max_length=10,
        label="Plate Number",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ABC1234'})
    )
    year_model = forms.IntegerField(
        label="Year Model",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 2020'})
    )
    color = forms.CharField(
        max_length=20,
        label="Color",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Red'})
    )
    type = forms.ChoiceField(
        choices=Vehicle.VEHICLE_TYPE,
        label="Vehicle Type",
        widget=forms.Select()
    )
    engine_number = forms.CharField(
        max_length=25,
        label="Motor/Engine Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter engine number'})
    )
    chassis_number = forms.CharField(
        max_length=17,
        label="Chassis Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter chassis number'})
    )
    or_number = forms.CharField(
        max_length=20,
        label='Official Receipt',
        widget=forms.TextInput(attrs={'placeholder': 'Enter OR Number'})
    )
    cr_number = forms.CharField(
        max_length=20,
        label='Certificate of Registration',
        widget=forms.TextInput(attrs={'placeholder': 'Enter CR Number'})
    )

    # Owner Information
    owner = forms.ChoiceField(
        choices=[('yes', 'Yes, I am the owner of the vehicle'),
                 ('no', 'No, I am registering on behalf of the owner')],
        label="Are you the owner of this vehicle?",
        widget=forms.RadioSelect()
    )
    owner_firstname = forms.CharField(
        max_length=45,
        required=False,
        label="Owner's First Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's first name"})
    )
    owner_middlename = forms.CharField(
        max_length=45,
        required=False,
        label="Owner's Middle Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's middle name"})
    )
    owner_lastname = forms.CharField(
        max_length=45,
        required=False,
        label="Owner's Last Name",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's last name"})
    )
    owner_suffix = forms.CharField(
        max_length=5,
        required=False,
        label="Owner's Suffix",
        widget=forms.TextInput(attrs={'placeholder': "e.g. Jr"})
    )
    relationship_to_owner = forms.CharField(
        max_length=15,
        required=False,
        label="Relationship to Owner",
        widget=forms.TextInput(attrs={'placeholder': "e.g. Father, Mother, etc."})
    )
    contact_number = forms.CharField(
        max_length=13,
        required=False,
        label="Owner's Contact Number",
        widget=forms.TextInput(attrs={'placeholder': "e.g. 09123456789"})
    )
    address = forms.CharField(
        max_length=75,
        required=False,
        label="Owner's Address",
        widget=forms.TextInput(attrs={'placeholder': "Enter owner's address"})
    )

    
    def clean(self):
        cleaned_data = super().clean()
        is_owner = cleaned_data.get("owner") == "yes"

        if not is_owner:
            required_fields = ["owner_firstname", "owner_lastname", "relationship_to_owner", "contact_number"]
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