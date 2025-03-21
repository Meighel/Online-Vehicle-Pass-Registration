from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, SecurityProfileForm, CashierProfileForm, AdminProfileForm
from .forms import VehicleForm, RegistrationForm, RegistrationStatusForm, VehiclePassForm, PaymentTransactionForm
from .forms import InspectionReportForm, NotificationForm, AnnouncementForm
from .models import UserProfile, SecurityProfile, CashierProfile, AdminProfile
from .models import Vehicle, Registration, VehiclePass, PaymentTransaction
from .models import InspectionReport, Notification, Announcement
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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

class UserPageView(ListView):
    model = UserProfile
    context_object_name = "user"
    template_name = "user.html"



class SecurityPageView(ListView):
    model = SecurityProfile
    context_object_name = "security"
    template_name = "security.html"

class CashierPageView(ListView):
    model = CashierProfile
    context_object_name = "cashier"
    template_name = "cashier.html"

class AdminPageView(ListView):
    model = AdminProfile
    context_object_name = "admin"
    template_name = "admin.html"

######VEHICLE REGISTRATION VIEW AND CRUD ############
#####################################################
class VehiclePageView(ListView):
    model = Vehicle 
    context_object_name = "vehicle"
    template_name = "vehicle.html"

class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicle_form.html"
    success_url = reverse_lazy('vehicle')

    def form_valid(self,form):
        plate_number = form.instance.plate_Number
        messages.success(self.request, f'{plate_number} has been successfully updated.')

        return super().form_valid(form)

class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicle_edit.html"
    success_url = reverse_lazy('vehicle')

    def form_valid(self,form):
        plate_number = form.instance
        messages.success(self.request, f'{plate_number} has been successfully updated.')

        return super().form_valid(form)
    
class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = "vehicle_delete.html"
    success_url = reverse_lazy('vehicle')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully deleted.')
        return super().form_valid(form)



######REGISTRATION VIEW AND CRUD
################################   
class RegistrationView(ListView):
    model = Registration
    context_object_name = "registration"
    template_name = ""

# class RegistrationStatusView(ListView):
#     model = RegistrationStatus
#     context_object_name = "registration_status"
#     template_name = ""

class VehiclePassView(ListView):
    model = VehiclePass
    context_object_name = "vehicle_pass"
    template_name = ""

class PaymentView(ListView):
    model = PaymentTransaction
    context_object_name = "payment"
    template_name = ""

class InspectionReportView(ListView):
    model = InspectionReport
    context_object_name = "inspection_report"
    template_name = ""

class NotificationView(ListView):
    model = Notification
    context_object_name = "notification"
    template_name = ""

class AnnouncementView(ListView):
    model = Announcement
    context_object_name = "announcement"
    template_name = ""
