from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserSignupForm, AdminUserForm
# from .forms import UserRegistrationForm, UserProfileForm, SecurityProfileForm, CashierProfileForm, AdminProfileForm
# from .forms import VehicleForm, RegistrationForm, RegistrationStatusForm, VehiclePassForm, PaymentTransactionForm
# from .forms import InspectionReportForm, NotificationForm, AnnouncementForm
from .models import UserProfile, SecurityProfile, CashierProfile, AdminProfile
from .models import Vehicle, Registration, VehiclePass, PaymentTransaction
from .models import InspectionReport, Notification, Announcement
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .authentication import login_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(corporate_email=email)
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("login")  # Redirect back to login on failure

        if user.check_password(password):  # Check hashed password
            request.session["user_id"] = user.id  # Store user ID in session
            return redirect_user_dashboard(user)  # Redirect based on role
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")  # Redirect back to login

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login") 


def redirect_user_dashboard(user):
    """Redirects the user based on their role."""
    if SecurityProfile.objects.filter(user=user).exists():
        return redirect("security_dashboard")
    elif CashierProfile.objects.filter(user=user).exists():
        return redirect("cashier_dashboard")
    elif AdminProfile.objects.filter(user=user).exists():
        return redirect("admin_dashboard")
    
    return redirect("default_dashboard")


@login_required
def default_dashboard(request):
    return render(request, "User Dashboard/User_Dashboard.html")

@login_required
def security_dashboard(request):
    return render(request, "Security Dashboard/Security_Dashboard.html")

@login_required
def cashier_dashboard(request):
    return render(request, "Cashier Dashboard/Cashier_Dashboard.html")

@login_required
def admin_dashboard(request):
    return render(request, "Admin Dashboard/Admin_Dashboard.html")

@login_required
def admin_manage_user(request):
    return render(request, "Admin Dashboard/Admin_Manage_User.html")

@login_required
def admin_manage_application(request):
    return render(request, "Admin Dashboard/Admin_Application.html")

@login_required
def admin_manage_payments(request):
    return render(request, "Admin Dashboard/Admin_Manage_Payment.html")


def signup_view(request):
    email = request.GET.get('email_value', '')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully signed up! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "There was an error with your signup. Please try again.")
    else:
        form = UserSignupForm(initial={'corporate_email': email})  
    
    # Pass the email_value directly to the template
    return render(request, 'signup.html', {'form': form, 'email_value': email})

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             role = user_form.cleaned_data['role']
#             user.save()

#             # Create role-specific profile
#             if role == 'user':
#                 profile_form = UserProfileForm(request.POST)
#             elif role == 'security':
#                 profile_form = SecurityProfileForm(request.POST)
#             elif role == 'cashier':
#                 profile_form = CashierProfileForm(request.POST)
#             elif role == 'admin':
#                 profile_form = AdminProfileForm(request.POST)
#             else:
#                 profile_form = None

#             if profile_form and profile_form.is_valid():
#                 profile = profile_form.save(commit=False)
#                 profile.user = user
#                 profile.save()

#             messages.success(request, 'Registration successful!')
#             return redirect('login')

#     else:
#         user_form = UserRegistrationForm()
#         profile_form = None  # Will be initialized based on role

#     return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


#### ADMIN  PAGE ####

###### Dashboard

###### Manage Users
class AdminViewUser(ListView):
    model = UserProfile
    context_object_name = "admin_dashboard"
    template_name = 'Admin Dashboard/Admin_Dashboard.html'

class AdminCreateUser(CreateView):
    model = UserProfile
    form_class = AdminUserForm
    template_name = "Forms/forms_1.html"
    success_url  = reverse_lazy("admin_create_user")

class AdminUpdateUser(UpdateView):
    model = UserProfile
    form_class = AdminUserForm
    template_name = "Forms/forms_1.html"
    success_url  = reverse_lazy("admin_update_user")

class AdminUpdateUser(DeleteView):
    model = UserProfile
    template_name = ""
    success_url  = reverse_lazy("admin_delete_user")

###### Payments

###### Passes

###### Reports


# class SecurityPageView(ListView):
#     model = SecurityProfile
#     context_object_name = "security"
#     template_name = "security.html"

# class CashierPageView(ListView):
#     model = CashierProfile
#     context_object_name = "cashier"
#     template_name = "cashier.html"

# class AdminPageView(ListView):
#     model = AdminProfile
#     context_object_name = "admin"
#     template_name = "admin.html"

# ######VEHICLE REGISTRATION VIEW AND CRUD ############
# #####################################################
# class VehiclePageView(ListView):
#     model = Vehicle 
#     context_object_name = "vehicle"
#     template_name = "vehicle.html"

# class VehicleCreateView(CreateView):
#     model = Vehicle
#     form_class = VehicleForm
#     template_name = "vehicle_form.html"
#     success_url = reverse_lazy('vehicle')

#     def form_valid(self,form):
#         plate_number = form.instance.plate_Number
#         messages.success(self.request, f'{plate_number} has been successfully updated.')

#         return super().form_valid(form)

# class VehicleUpdateView(UpdateView):
#     model = Vehicle
#     form_class = VehicleForm
#     template_name = "vehicle_edit.html"
#     success_url = reverse_lazy('vehicle')

#     def form_valid(self,form):
#         plate_number = form.instance
#         messages.success(self.request, f'{plate_number} has been successfully updated.')

#         return super().form_valid(form)
    
# class VehicleDeleteView(DeleteView):
#     model = Vehicle
#     template_name = "vehicle_delete.html"
#     success_url = reverse_lazy('vehicle')

#     def form_valid(self, form):
#         messages.success(self.request, 'Successfully deleted.')
#         return super().form_valid(form)



# ######REGISTRATION VIEW AND CRUD
# ################################   
# class RegistrationView(ListView):
#     model = Registration
#     context_object_name = "registration"
#     template_name = ""

# class RegistrationStatusView(ListView):
#     model = RegistrationStatus
#     context_object_name = "registration_status"
#     template_name = ""

# class VehiclePassView(ListView):
#     model = VehiclePass
#     context_object_name = "vehicle_pass"
#     template_name = ""

# class PaymentView(ListView):
#     model = PaymentTransaction
#     context_object_name = "payment"
#     template_name = ""

# class InspectionReportView(ListView):
#     model = InspectionReport
#     context_object_name = "inspection_report"
#     template_name = ""

# class NotificationView(ListView):
#     model = Notification
#     context_object_name = "notification"
#     template_name = ""

# class AnnouncementView(ListView):
#     model = Announcement
#     context_object_name = "announcement"
#     template_name = ""