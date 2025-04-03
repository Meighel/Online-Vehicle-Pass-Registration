from django import forms
from .models import UserProfile
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
    

# # from django.contrib.auth.forms import UserCreationForm
# from .models import (UserProfile, SecurityProfile, CashierProfile, 
#                      AdminProfile, Vehicle, Registration, VehiclePass,
#                      PaymentTransaction, InspectionReport, Notification, Announcement)

# class UserRegistrationForm(UserCreationForm):
#     role = forms.ChoiceField(choices=CustomUser.role_choices, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ['corporate_email', 'password1', 'password2', 'role']

#     def clean_corporate_email(self):
#         email = self.cleaned_data.get('corporate_email')
#         if CustomUser.objects.filter(corporate_email=email).exists():
#             raise forms.ValidationError("This email is already registered.")
#         return email

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

# class SecurityProfileForm(forms.ModelForm):
#     class Meta:
#         model = SecurityProfile
#         fields = '__all__'

# class CashierProfileForm(forms.ModelForm):
#     class Meta:
#         model = CashierProfile
#         fields = '__all__'

# class AdminProfileForm(forms.ModelForm):
#     class Meta:
#         model = AdminProfile
#         fields = '__all__'

# class VehicleForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super().clean()
#         owner = cleaned_data.get('owner')
#         if owner and Vehicle.objects.filter(owner=owner).count() >= 2:
#             raise forms.ValidationError('You can only register up to two vehicles.')
#         return cleaned_data

# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = '__all__'

# class VehiclePassForm(forms.ModelForm):
#     class Meta:
#         model = VehiclePass
#         fields = '__all__'

# class PaymentTransactionForm(forms.ModelForm):
#     class Meta:
#         model = PaymentTransaction
#         fields = '__all__'

# class InspectionReportForm(forms.ModelForm):
#     class Meta:
#         model = InspectionReport
#         fields = '__all__'

# class NotificationForm(forms.ModelForm):
#     class Meta:
#         model = Notification
#         fields = '__all__'

# class AnnouncementForm(forms.ModelForm):
#     class Meta:
#         model = Announcement
#         fields = '__all__'
