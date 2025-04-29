from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
<<<<<<< HEAD
from .forms import UserSignupForm, AdminUserForm, AdminPaymentForm, AdminRegistrationForm, AdminPassForm, AdminReportForm
=======
from .forms import (UserSignupForm, UserProfileForm, 
                    PaymentTransactionForm,
                    ApplicationForm,
                    InspectionApprovalForm,
                    VehicleRegistrationStep1Form, VehicleRegistrationStep2Form, VehicleRegistrationStep3Form,
)
>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039
from .models import UserProfile, SecurityProfile, CashierProfile, AdminProfile
from .models import Vehicle, Registration, VehiclePass, PaymentTransaction
from .models import InspectionReport, Notification, Announcement, Owner
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .authentication import login_required, CustomLoginRequiredMixin
from django.contrib.auth import logout
<<<<<<< HEAD
from django.contrib.auth.mixins import LoginRequiredMixin
=======
from .authentication import login_required, CustomLoginRequiredMixin
>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039

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
    user_id = request.session.get("user_id")
    
    try:
        profile = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        profile = None
    
    # Get the latest registration
    try:
        registration = Registration.objects.filter(user=profile).latest('created_at')
    except Registration.DoesNotExist:
        registration = None
    
    # Get application history
    history = Registration.objects.filter(user=profile).order_by('-created_at')
    
    context = {
        'profile': profile,
        'registration': registration,
        'history': history,
    }
    
    return render(request, "User Dashboard/User_Dashboard.html", context)

@login_required
def user_application(request):
    return render(request, "User Dashboard/User_Application.html")

@login_required
def vehicle_registration_step_1(request):
    user_id = request.session.get("user_id")
    user = UserProfile.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = VehicleRegistrationStep1Form(request.POST)
        if form.is_valid():
            # Store data in session for later use
            step1_data = form.cleaned_data
            request.session['step1_data'] = {
                'first_name': step1_data['first_name'],
                'middle_name': step1_data['middle_name'],
                'last_name': step1_data['last_name'],
                'corporate_email': step1_data['corporate_email'],
                'role': step1_data['role'],
                'driver_license_number': step1_data['driver_license_number'],
                'vehicle_type': step1_data['vehicle_type'],
                'model': step1_data['model'],
                'plate_number': step1_data['plate_number'],
                'chassis_number': step1_data['chassis_number'],
                'or_number': step1_data['or_number'],
                'cr_number': step1_data['cr_number']
            }
            return redirect('vehicle_registration_step_2')
    else:
        # Pre-fill form with user data if available
        initial_data = {
            'first_name': user.firstname,
            'middle_name': user.middle_name,
            'last_name': user.lastname,
            'corporate_email': user.corporate_email,
            'role': user.role,
            'driver_license_number': user.dl_number
        }
        form = VehicleRegistrationStep1Form(initial=initial_data)

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'forms/forms_1.html', context)

@login_required
def vehicle_registration_step_2(request):
    user_id = request.session.get("user_id")
    user = UserProfile.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = VehicleRegistrationStep2Form(request.POST)
        if form.is_valid():
            # Store owner data in session
            step2_data = form.cleaned_data
            request.session['step2_data'] = {
                'is_owner': step2_data['owner'] == 'yes',
                'owner_first_name': step2_data.get('owner_first_name', ''),
                'owner_middle_name': step2_data.get('owner_middle_name', ''),
                'owner_last_name': step2_data.get('owner_last_name', ''),
                'owner_contact_number': step2_data.get('owner_contact_number', '')
            }
            return redirect('vehicle_registration_step_3')
    else:
        form = VehicleRegistrationStep2Form()

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'forms/forms_2.html', context)

@login_required
def vehicle_registration_step_3(request):
    user_id = request.session.get("user_id")
    user = UserProfile.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = VehicleRegistrationStep3Form(request.POST)
        if form.is_valid():
            google_folder_link = form.cleaned_data['google_drive_link']
            
            try:
                # Get data from previous steps
                step1_data = request.session.get('step1_data', {})
                step2_data = request.session.get('step2_data', {})
                
                # Save to database
                # 1. First determine if we need to create an Owner object
                owner = None
                if not step2_data.get('is_owner', True):
                    # Create owner object
                    owner = Owner.objects.create(
                        owner_firstname=step2_data['owner_first_name'],
                        owner_middlename=step2_data['owner_middle_name'],
                        owner_lastname=step2_data['owner_last_name'],
                        owner_contact_number=step2_data['owner_contact_number'],
                        relationship_to_owner="User Relationship"  
                    )
                
                # 2. Create Vehicle object
                vehicle = Vehicle.objects.create(
                    self_ownership=user if step2_data.get('is_owner', True) else None,
                    legal_owner=None if step2_data.get('is_owner', True) else owner,
                    plateNumber=step1_data['plate_number'],
                    type=step1_data['vehicle_type'],
                    model=step1_data['model'],
                    color="Not Specified",  # You might want to add this to your form
                    chassisNumber=step1_data['chassis_number'],
                    OR_Number=step1_data['or_number'],
                    CR_Number=step1_data['cr_number']
                )
                
                # 3. Create Registration object
                registration = Registration.objects.create(
                    user=user,
                    vehicle=vehicle,
                    files=google_folder_link,
                    status='pending'
                )
                
                # Clear session data
                for key in ['step1_data', 'step2_data']:
                    if key in request.session:
                        del request.session[key]
                
                messages.success(request, "Vehicle registration submitted successfully!")
                return redirect('user_pass_status')
                
            except Exception as e:
                messages.error(request, f"Error saving registration: {str(e)}")
                
    else:
        form = VehicleRegistrationStep3Form()

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'forms/forms_3.html', context)

def registration_complete(request):
    return render(request, 'User Dasgboard/User_Pass_Status')

@login_required
def user_pass_status(request):
    return render(request, "User Dashboard/User_Pass_Status.html")

# Admin Page View 
@login_required
def admin_dashboard(request):
    return render(request, "Admin Dashboard/Admin_Dashboard.html")

<<<<<<< HEAD
# @login_required
# def admin_manage_user(request):
#     return render(request, "Admin Dashboard/Admin_Manage_User.html") 
=======

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
    

>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039

# @login_required
# def admin_manage_application(request):
#     return render(request, "Admin Dashboard/Admin_Application.html")

<<<<<<< HEAD
# @login_required
# def admin_manage_payments(request):
#     return render(request, "Admin Dashboard/Admin_Manage_Payment.html")
=======

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
    vehicle_passes = VehiclePass.objects.select_related('vehicle__self_ownership').all()

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
>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039


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
    paginate_by = 5

    def get_queryset(self):
        return PaymentTransaction.objects.filter(status='pending')
    
    
class cashierViewTransaction(CustomLoginRequiredMixin, ListView):
    model = PaymentTransaction
    template_name = "Cashier Dashboard/Cashier_Transaction.html"
    context_object_name = 'transaction_list'
    paginate_by = 5

    def get_queryset(self):
        return PaymentTransaction.objects.exclude(status='pending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user ID from the session
        user_id = self.request.session.get('user_id')
        
        # Get the actual UserProfile instance
        if user_id:
            user_profile = UserProfile.objects.get(id=user_id)
            context['form'] = PaymentTransactionForm(user=user_profile)
        else:
            context['form'] = PaymentTransactionForm()
        
        return context


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

<<<<<<< HEAD
#### ADMIN  PAGE ####

###### Dashboard
## charts

###### Manage Users
class AdminViewUser(CustomLoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = "admin_manage_user"
    template_name = 'Admin Dashboard/Admin_Manage_User.html'
    paginate_by = 3

class AdminCreateUser(CustomLoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = AdminUserForm
    template_name = "Forms/forms_1.html" 
    success_url  = reverse_lazy("")

class AdminUpdateUser(CustomLoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = AdminUserForm
    template_name = "Forms/forms_1.html" #placeholder lang baka need pa ng specific update form 
    success_url  = reverse_lazy("")

class AdminDeleteUser(CustomLoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = "" ##walang template para sa deletion
    success_url  = reverse_lazy("")

###### Application
class AdminViewApplication(CustomLoginRequiredMixin, ListView):
    model = Registration
    context_object_name = "admin_manage_application"
    template_name = 'Admin Dashboard/Admin_Application.html'

class AdminCreateApplication(CustomLoginRequiredMixin, CreateView):
    model = Registration
    form_class = AdminRegistrationForm
    template_name = "" #application form 
    success_url  = reverse_lazy("")

class AdminUpdateApplication(CustomLoginRequiredMixin, UpdateView):
    model = Registration
    form_class = AdminRegistrationForm
    template_name = "" #application form 
    success_url  = reverse_lazy("")

class AdminDeleteApplication(CustomLoginRequiredMixin, DeleteView):
    model = Registration
    template_name = "" #application delete form
    success_url  = reverse_lazy("")

###### Payment
class AdminViewPayment(CustomLoginRequiredMixin, ListView):
    model = PaymentTransaction
    context_object_name = "admin_manage_payments"
    template_name = 'Admin Dashboard/Admin_Manage_Payment.html'

class AdminCreatePayment(CustomLoginRequiredMixin, CreateView):
    model = PaymentTransaction
    form_class = AdminPaymentForm
    template_name = "" #payment form
    success_url  = reverse_lazy("")

class AdminUpdatePayment(CustomLoginRequiredMixin, UpdateView):
    model = PaymentTransaction
    form_class = AdminPaymentForm
    template_name = "" # payment form 
    success_url  = reverse_lazy("")

class AdminDeletePayment(CustomLoginRequiredMixin,DeleteView):
    models = PaymentTransaction
    template_name = "" #payment delete form
    success_url  = reverse_lazy("")

###### Passes
class AdminViewPasses(CustomLoginRequiredMixin, ListView):
    model = VehiclePass
    context_object_name = "admin_manage_passes"
    template_name = 'Admin Dashboard/Admin_Manage_Passes.html'

class AdminCreatePasses(CustomLoginRequiredMixin, CreateView):
    model = VehiclePass
    form_class = AdminPassForm
    template_name = "" #passes forms 
    success_url  = reverse_lazy("")

class AdminUpdatePasses(CustomLoginRequiredMixin, UpdateView):
    model = VehiclePass
    form_class = AdminPassForm
    template_name = "" # passes forms
    success_url = reverse_lazy("")

class AdminDeletePasses(CustomLoginRequiredMixin, DeleteView):
    model = VehiclePass
    template_name = "" #passes delete form
    success_url  = reverse_lazy("")
###### Reports
class AdminViewReport(CustomLoginRequiredMixin, ListView):
    model = InspectionReport
    context_object_name = "admin_manage_reports"
    template_name = 'Admin Dashboard/Admin_Reports.html'

class AdminCreateReport(CustomLoginRequiredMixin, CreateView):
    model = InspectionReport
    form_class = AdminReportForm
    template_name = "" #report forms
    success_url  = reverse_lazy("")

class AdminUpdateReport(CustomLoginRequiredMixin, UpdateView):
    model = InspectionReport
    form_class = AdminReportForm
    template_name = ""#template form
    success_url  = reverse_lazy("")

class AdminDeleteReport(CustomLoginRequiredMixin, DeleteView):
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
=======
class SecurityViewStickers(CustomLoginRequiredMixin, ListView):
    model = VehiclePass
    template_name = 'Security Dashboard/Security_Release_Stickers.html'
    context_object_name = 'stickers'
    paginate_by = 5

@login_required
def security_report(request):
    return render(request, "Security Dashboard/Security_History.html")
>>>>>>> ec30462a99f86741fe8ee4b84dd0f360fc231039
