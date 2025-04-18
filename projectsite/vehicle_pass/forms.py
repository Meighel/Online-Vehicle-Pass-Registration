from django import forms
from .models import (UserProfile,
                     PaymentTransaction,
                     Registration,
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

class InspectionApprovalForm(forms.ModelForm):
    class Meta:
        model = InspectionReport
        fields = ['remarks', 'additional_notes', 'is_approved']