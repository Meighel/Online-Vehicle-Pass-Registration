from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import (UserSignupForm, UserProfileForm, 
                    PaymentTransactionForm,
                    ApplicationForm,
                    InspectionApprovalForm,
                    VehicleRegistrationStep1Form, VehicleRegistrationStep2Form, VehicleRegistrationStep3Form,
)
from .models import UserProfile, SecurityProfile, CashierProfile, AdminProfile
from .models import Vehicle, Registration, VehiclePass, PaymentTransaction
from .models import InspectionReport, Notification, Announcement
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .authentication import login_required
from django.contrib.auth import logout
from .authentication import login_required, CustomLoginRequiredMixin

def home(request):
    return render(request, 'index.html')

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
def user_application(request):
    return render(request, "User Dashboard/User_Application.html")

def vehicle_registration_step_1(request):
    if request.method == 'POST':
        form = VehicleRegistrationStep1Form(request.POST)
        if form.is_valid():
            # Handle form data here or store it in the session
            request.session['step1_data'] = form.cleaned_data
            return redirect('vehicle_registration_step_2')
    else:
        form = VehicleRegistrationStep1Form()

    return render(request, 'forms/forms_1.html', {'form': form})

def vehicle_registration_step_2(request):
    if request.method == 'POST':
        form = VehicleRegistrationStep2Form(request.POST)
        if form.is_valid():
            # Handle form data here or store it in the session
            request.session['step2_data'] = form.cleaned_data
            return redirect('vehicle_registration_step_3')
    else:
        form = VehicleRegistrationStep2Form()

    return render(request, 'forms/forms_2.html', {'form': form})

def vehicle_registration_step_3(request):
    if request.method == 'POST':
        form = VehicleRegistrationStep3Form(request.POST)
        if form.is_valid():
            # Handle form data here or store it in the session
            request.session['step3_data'] = form.cleaned_data
            return redirect('user_pass_status')
    else:
        form = VehicleRegistrationStep3Form()

    return render(request, 'forms/forms_3.html', {'form': form})

def registration_complete(request):
    return render(request, 'User Dasgboard/User_Pass_Status')

@login_required
def user_pass_status(request):
    return render(request, "User Dashboard/User_Pass_Status.html")

# Admin Page View 
@login_required
def admin_dashboard(request):
    return render(request, "Admin Dashboard/Admin_Dashboard.html")


class AdminViewUser(CustomLoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = "users"
    template_name = 'Admin Dashboard/Admin_Manage_User.html'
    paginate_by = 5

class AdminCreateUser(CustomLoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "Admin Dashboard/Admin User CRUD/Admin_Create_User.html" 
    success_url  = reverse_lazy("admin_manage_user")
    
class AdminUpdateUser(CustomLoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "Admin Dashboard/Admin User CRUD/Admin_Update_User.html"
    success_url  = reverse_lazy("admin_manage_user")
    
class AdminDeleteUser(CustomLoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = "Admin Dashboard/Admin User CRUD/Admin_Delete_User.html"
    success_url = reverse_lazy('admin_manage_user')

    def form_valid(self, form):
        messages.success(self.request, 'Deleted successfully. ')
        return super().form_valid(form)

class AdminViewSpecificUser(CustomLoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'Admin Dashboard/Admin User CRUD/Admin_View_Specific_User.html'
    context_object_name = 'user'
    


@login_required
def admin_manage_application(request):
    return render(request, "Admin Dashboard/Admin_Application.html")


# CRUD AND VIEW OF TRANSACTION AND PAYMENT
class adminViewPayment(ListView):
    model = PaymentTransaction
    template_name = "Admin Dashboard/Admin_Manage_Payment.html"
    context_object_name = 'payment_list'
    paginate_by = 5

    def get_queryset(self):
        return PaymentTransaction.objects.filter(status='pending')
    
class adminViewTransaction(ListView):
    model = PaymentTransaction
    template_name = "Admin Dashboard/Admin_Transaction.html"
    context_object_name = 'transaction_list'
    paginate_by = 5

    def get_queryset(self):
        return PaymentTransaction.objects.exclude(status='pending')
    
class adminUpdatePayment(UpdateView):
    model = PaymentTransaction
    form_class = PaymentTransactionForm
    template_name ="Admin Dashboard/Admin_Payment_Update.html"
    success_url = reverse_lazy("admin_payments")

@login_required
def admin_manage_passes(request):
    # Fetch all vehicle passes and related data
    vehicle_passes = VehiclePass.objects.select_related('vehicle__owner').all()

    context = {
        'vehicle_passes': vehicle_passes,
    }
    return render(request, "Admin Dashboard/Admin_Manage_Passes.html", context)

@login_required
def admin_report(request):
    return render (request, "Admin Dashboard/Admin_Reports.html")

class AdminViewApplication(CustomLoginRequiredMixin, ListView):
    model = Registration
    template_name = 'Admin Dashboard/Admin_Application.html'
    context_object_name = 'applications'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = context['applications']
        print(f"Applications count: {len(applications)}")
        if applications:
            print(f"First application: {applications[0]}")
        return context


class AdminViewSpecificApplication(CustomLoginRequiredMixin, DetailView):
    model = Registration
    template_name = 'Admin Dashboard/Admin Application CRUD/Admin_View_Specific_Application.html'
    context_object_name = 'applications'


class AdminUpdateApplication(CustomLoginRequiredMixin, UpdateView):
    model = Registration
    form_class = ApplicationForm
    template_name = 'Admin Dashboard/Admin Application CRUD/Admin_Update_Application.html'
    success_url = reverse_lazy('admin_manage_application')


# Cashier Page View 
@login_required
def cashier_dashboard(request):
    return render(request, "Cashier Dashboard/Cashier_Dashboard.html")


class cashierViewPayment(CustomLoginRequiredMixin, ListView):
    model = PaymentTransaction
    template_name = "Cashier Dashboard/Cashier_Payment.html"
    context_object_name = 'payment_list'
    paginate_by = 10

    def get_queryset(self):
        return PaymentTransaction.objects.filter(status='pending')
    
    
class cashierViewTransaction(CustomLoginRequiredMixin, ListView):
    model = PaymentTransaction
    template_name = "Cashier Dashboard/Cashier_Transaction.html"
    context_object_name = 'transaction_list'
    paginate_by = 10

    def get_queryset(self):
        return PaymentTransaction.objects.exclude(status='pending')


class cashierUpdatePayment(CustomLoginRequiredMixin, UpdateView):
    model = PaymentTransaction
    form_class = PaymentTransactionForm
    template_name ="Cashier Dashboard/Cashier_Payment_Update.html"
    success_url = reverse_lazy("cashier_payments")

@login_required
def cashier_report(request):
    return render(request, "Cashier Dashboard/Cashier_Reports.html")

# Security Page Vies
@login_required
def security_dashboard(request):
    return render(request, "Security Dashboard/Security_Dashboard.html")

@login_required
def security_manage_application(request):
    return render(request, "Security Dashboard/Security_Application.html")

class SecurityViewApplication(CustomLoginRequiredMixin, ListView):
    model = Registration
    template_name = 'Security Dashboard/Security_Application.html'
    context_object_name = 'applications'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = context['applications']
        print(f"Applications count: {len(applications)}")
        if applications:
            print(f"First application: {applications[0]}")
        return context

class SecurityViewSpecificApplication(CustomLoginRequiredMixin, DetailView):
    model = Registration
    template_name = 'Security Dashboard/Security Application CRUD/Security_View_Specific_Application.html'
    context_object_name = 'registration'


class SecurityUpdateApplication(CustomLoginRequiredMixin, UpdateView):
    model = Registration
    form_class = ApplicationForm
    template_name = 'Security Dashboard/Security Application CRUD/Security_Update_Application.html'
    success_url = reverse_lazy('security_manage_application')

@login_required
def security_manage_inspection(request):
    return render(request, "Security Dashboard/Security_Inspection.html")

class SecurityViewInspectionReports(CustomLoginRequiredMixin, ListView):
    model = InspectionReport
    template_name = 'Security Dashboard/Security_Inspection.html'
    context_object_name = 'inspections'
    paginate_by = 5

    def get_queryset(self):
        return InspectionReport.objects.exclude(remarks='sticker_released')

def handle_inspection_action(request):
    if request.method == "POST":
        inspection_id = request.POST.get('inspection_id')
        action = request.POST.get('action')
        additional_notes = request.POST.get('additional_notes', '')
        
        if inspection_id and action:
            try:
                inspection = InspectionReport.objects.get(id=inspection_id)
                inspection.additional_notes = additional_notes
                
                if action == 'approve':
                    inspection.is_approved = True
                    inspection.remarks = 'sticker_released'
                elif action == 'reject':
                    inspection.is_approved = False
                    inspection.remarks = 'application_declined'
                    
                inspection.save()
                messages.success(request, f"Inspection {action}d successfully.")
            except InspectionReport.DoesNotExist:
                messages.error(request, "Inspection record not found.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Missing required parameters.")
    
    return redirect('security_manage_inspection')

class SecurityViewStickers(CustomLoginRequiredMixin, ListView):
    model = VehiclePass
    template_name = 'Security Dashboard/Security_Release_Stickers.html'
    context_object_name = 'stickers'
    paginate_by = 5

@login_required
def security_report(request):
    return render(request, "Security Dashboard/Security_History.html")
