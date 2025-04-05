from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserSignupForm, AdminUserForm, AdminPaymentForm, AdminRegistrationForm, AdminPassForm, AdminReportForm
from .models import UserProfile, SecurityProfile, CashierProfile, AdminProfile
from .models import Vehicle, Registration, VehiclePass, PaymentTransaction
from .models import InspectionReport, Notification, Announcement
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .authentication import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

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

#### ADMIN  PAGE ####

###### Dashboard
## charts

###### Manage Users
class AdminViewUser(LoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = "admin_dashboard"
    template_name = 'Admin Dashboard/Admin_Dashboard.html'
    paginate_by = 3

class AdminCreateUser(LoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = AdminUserForm
    template_name = "Forms/forms_1.html" 
    success_url  = reverse_lazy("")

class AdminUpdateUser(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = AdminUserForm
    template_name = "Forms/forms_1.html" #placeholder lang baka need pa ng specific update form 
    success_url  = reverse_lazy("")

class AdminDeleteUser(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = "" ##walang template para sa deletion
    success_url  = reverse_lazy("")

###### Application
class AdminViewApplication(LoginRequiredMixin, ListView):
    model = Registration
    context_object_name = "admin_manage_application"
    template_name = 'Admin Dashboard/Admin_Application.html'

class AdminCreateApplication(LoginRequiredMixin, CreateView):
    model = Registration
    form_class = AdminRegistrationForm
    template_name = "" #application form 
    success_url  = reverse_lazy("")

class AdminUpdateApplication(LoginRequiredMixin, UpdateView):
    model = Registration
    form_class = AdminRegistrationForm
    template_name = "" #application form 
    success_url  = reverse_lazy("")

class AdminDeleteApplication(LoginRequiredMixin, DeleteView):
    model = Registration
    template_name = "" #application delete form
    success_url  = reverse_lazy("")

###### Payment
class AdminViewPayment(LoginRequiredMixin, ListView):
    model = PaymentTransaction
    context_object_name = "admin_manage_payments"
    template_name = 'Admin Dashboard/Admin_Manage_Payment.html'

class AdminCreatePayment(LoginRequiredMixin, CreateView):
    model = PaymentTransaction
    form_class = AdminPaymentForm
    template_name = "" #payment form
    success_url  = reverse_lazy("")

class AdminUpdatePayment(LoginRequiredMixin, UpdateView):
    model = PaymentTransaction
    form_class = AdminPaymentForm
    template_name = "" # payment form 
    success_url  = reverse_lazy("")

class AdminDeletePayment(LoginRequiredMixin,DeleteView):
    models = PaymentTransaction
    template_name = "" #payment delete form
    success_url  = reverse_lazy("")

###### Passes
class AdminViewPasses(LoginRequiredMixin, ListView):
    model = VehiclePass
    context_object_name = "admin_dashboard"
    template_name = 'Admin Dashboard/Admin_Manage_Passes.html'

class AdminCreatePasses(LoginRequiredMixin, CreateView):
    model = VehiclePass
    form_class = AdminPassForm
    template_name = "" #passes forms 
    success_url  = reverse_lazy("")

class AdminUpdatePasses(LoginRequiredMixin, UpdateView):
    model = VehiclePass
    form_class = AdminPassForm
    template_name = "" # passes forms
    success_url = reverse_lazy("")

class AdminDeletePasses(LoginRequiredMixin, DeleteView):
    model = VehiclePass
    template_name = "" #passes delete form
    success_url  = reverse_lazy("")
###### Reports
class AdminViewReport(ListView):
    model = InspectionReport
    context_object_name = "admin_dashboard"
    template_name = 'Admin Dashboard/Admin_Application.html'

class AdminCreateReport(LoginRequiredMixin, CreateView):
    model = InspectionReport
    form_class = AdminReportForm
    template_name = "" #report forms
    success_url  = reverse_lazy("")

class AdminUpdateReport(LoginRequiredMixin, UpdateView):
    model = InspectionReport
    form_class = AdminReportForm
    template_name = ""#template form
    success_url  = reverse_lazy("")

class AdminDeleteReport(LoginRequiredMixin, DeleteView):
    model = InspectionReport
    template_name = "" #report delete form
    success_url  = reverse_lazy("")


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