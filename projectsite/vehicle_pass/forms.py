# from django import forms
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
