from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, SecurityProfileForm, CashierProfileForm, AdminProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            role = user_form.cleaned_data['role']
            user.save()

            # Create role-specific profile
            if role == 'user':
                profile_form = UserProfileForm(request.POST)
            elif role == 'security':
                profile_form = SecurityProfileForm(request.POST)
            elif role == 'cashier':
                profile_form = CashierProfileForm(request.POST)
            elif role == 'admin':
                profile_form = AdminProfileForm(request.POST)
            else:
                profile_form = None

            if profile_form and profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

            messages.success(request, 'Registration successful!')
            return redirect('login')

    else:
        user_form = UserRegistrationForm()
        profile_form = None  # Will be initialized based on role

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})
