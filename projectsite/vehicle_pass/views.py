from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import (UserSignupForm, UserProfileForm, 
                    # PaymentTransactionForm,
                    ApplicationForm,
                    # InspectionApprovalForm, 
                    PasswordUpdateForm,
                    VehicleRegistrationStep1Form, VehicleRegistrationStep2Form, VehicleRegistrationStep3Form,
                    # FinalDateInspectionForm,
)
from .models import UserProfile, SecurityProfile, AdminProfile
from .models import Vehicle, Registration, VehiclePass
from .models import Notification, Announcement, PasswordResetCode, LoginActivity, SiteVisit
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .authentication import login_required
from django.contrib.auth import logout
from .authentication import login_required, CustomLoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from datetime import timedelta 

from django.db.models import Count, Q
from django.utils.timezone import now
import calendar
from django.db.models.functions import TruncMonth
from django.contrib.auth import update_session_auth_hash
from .models import SiteVisit, LoginActivity

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
            return redirect("login")

        if user.check_password(password):
            request.session["user_id"] = user.id
            return redirect_user_dashboard(user)
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login") 

def redirect_user_dashboard(user):
    """Redirects the user based on their role."""
    if SecurityProfile.objects.filter(user=user).exists():
        return redirect("security_dashboard")
    elif AdminProfile.objects.filter(user=user).exists():
        return redirect("admin_dashboard")
    
    return redirect("default_dashboard")

@csrf_protect
@require_http_methods(["GET", "POST"])
def forgot_password(request):
    """
    View to handle the first step of password reset process.
    User enters their email address to receive a reset code.
    """
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            user = UserProfile.objects.get(corporate_email=email)
            
            # Invalidate any existing unused codes for this user
            PasswordResetCode.objects.filter(
                user=user, 
                is_used=False
            ).update(is_used=True)
            
            # Generate a new code
            code = PasswordResetCode.generate_code()
            reset_code = PasswordResetCode.objects.create(user=user, code=code)
            
            # Send email with the code
            send_reset_code_email(user, code)
            
            # Redirect to the verification page
            return redirect(reverse('verify_reset_code') + f'?email={email}')
            
        except UserProfile.DoesNotExist:
            messages.error(request, "No account found with that email address.")
    
    return render(request, 'password_reset/forgot_password.html')

@csrf_protect
@require_http_methods(["GET", "POST"])
def verify_reset_code(request):
    """
    View to verify the reset code entered by the user.
    """
    email = request.GET.get('email')
    if not email:
        return redirect('forgot_password')
    
    if request.method == "POST":
        code = request.POST.get('code')
        
        try:
            user = UserProfile.objects.get(corporate_email=email)
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()
            
            if reset_code:
                # Mark the code as used
                reset_code.is_used = True
                reset_code.save()
                
                # Redirect to password reset page
                return redirect(reverse('reset_password') + f'?email={email}&code={code}')
            else:
                messages.error(request, "Invalid or expired code. Please try again.")
        
        except UserProfile.DoesNotExist:
            messages.error(request, "No account found with that email address.")
    
    return render(request, 'password_reset/verify_code.html', {'email': email})

@csrf_protect
@require_http_methods(["GET", "POST"])
def reset_password(request):
    """
    View to handle the actual password reset after code verification.
    """
    email = request.GET.get('email')
    code = request.GET.get('code')
    
    if not email or not code:
        return redirect('forgot_password')
    
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'password_reset/reset_password.html')
        
        try:
            user = UserProfile.objects.get(corporate_email=email)
            
            # Verify a reset code existed and was used
            reset_code_exists = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=True,
                expires_at__gt=timezone.now() - timedelta(minutes=15)  # Give a bit of buffer time
            ).exists()
            
            if reset_code_exists:
                # Update the password
                user.password = password  # Your save method will hash it
                user.save()
                
                messages.success(request, "Password has been reset successfully. You can now login with your new password.")
                return redirect('login')  # Redirect to login page
            else:
                messages.error(request, "Invalid reset request. Please restart the password reset process.")
                return redirect('forgot_password')
                
        except UserProfile.DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return redirect('forgot_password')
    
    return render(request, 'password_reset/reset_password.html')

def send_reset_code_email(user, code):
    """
    Helper function to send the reset code via email.
    """
    subject = "Password Reset Code"
    message = f"""
    Hello {user.firstname},
    
    You requested a password reset for your account.
    
    Your password reset code is: {code}
    
    This code will expire in 10 minutes.
    
    If you did not request this password reset, please ignore this email.
    
    Regards,
    From Veripass Official
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.corporate_email]
    
    send_mail(subject, message, from_email, recipient_list)

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

    # # Fix: Avoid accessing userprofile on AnonymousUser
    # inspection = None
    # if profile:
    #     inspection = InspectionReport.objects.filter(
    #         payment_number__registration__user=profile
    #     ).last()  # Get latest one (if any)

    context = {
        'profile': profile,
        'registration': registration,
        'history': history,
        # 'inspection': inspection,
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
            step1_data = form.cleaned_data
            # Save Step 1 data into session
            request.session['step1_data'] = {
                # Personal Information
                'lastname': step1_data['lastname'],
                'firstname': step1_data['firstname'],
                'middlename': step1_data['middlename'],
                'suffix': step1_data['suffix'],
                'address': step1_data['address'],
                'contact': step1_data['contact'],
                'corporate_email': step1_data['corporate_email'],
                'school_role': step1_data['school_role'],

                # Employees
                'position': step1_data['position'],
                'workplace': step1_data['workplace'],

                # Students
                'college': step1_data['college'],
                'program': step1_data['program'],

                # Family Info
                'father_name': step1_data['father_name'],
                'father_contact': step1_data['father_contact'],
                'father_address': step1_data['father_address'],
                'mother_name': step1_data['mother_name'],
                'mother_contact': step1_data['mother_contact'],
                'mother_address': step1_data['mother_address'],
                'guardian_name': step1_data['guardian_name'],
                'guardian_contact': step1_data['guardian_contact'],
                'guardian_address': step1_data['guardian_address'],
            }
            return redirect('vehicle_registration_step_2')
    else:
        # Pre-fill form with user profile data if available
        initial_data = {
            'firstname': user.firstname,
            'middlename': user.middlename,
            'lastname': user.lastname,
            'suffix': user.suffix,
            'address': user.address,
            'dl_number': user.dl_number,
            'contact': user.contact,
            'corporate_email': user.corporate_email,
            'school_role': user.school_role,
            'position': getattr(user, 'position', ''),
            'workplace': getattr(user, 'workplace', ''),
            'college': getattr(user, 'college', ''), 
            'program': getattr(user, 'program', ''),
            'year_level':getattr(user, 'year_level', ''),
            # Family info may be blank initially
            'father_name': getattr(user, 'father_name', ''),
            'father_contact': getattr(user, 'father_contact', ''),
            'father_address': getattr(user, 'father_address', ''),
            'mother_name': getattr(user, 'mother_name', ''),
            'mother_contact': getattr(user, 'mother_contact', ''),
            'mother_address': getattr(user, 'mother_address', ''),
            'guardian_name': getattr(user, 'guardian_name', ''),
            'guardian_contact': getattr(user, 'guardian_contact', ''),
            'guardian_address': getattr(user, 'guardian_address', ''),
        }
        form = VehicleRegistrationStep1Form(initial=initial_data)

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'Forms/forms_1.html', context)

# views.py
@login_required
def vehicle_registration_step_2(request):
    user_id = request.session.get("user_id")
    user = UserProfile.objects.get(id=user_id)

    if request.method == 'POST':
        form = VehicleRegistrationStep2Form(request.POST)
        if form.is_valid():
            step2_data = form.cleaned_data

            # Save Step 2 data into session
            request.session['step2_data'] = {
                # Vehicle Information
                'make_model': step2_data['make_model'],
                'plate_number': step2_data['plate_number'],
                'year_model': step2_data['year_model'],
                'color': step2_data['color'],
                'type': step2_data['type'],
                'engine_number': step2_data['engine_number'],
                'chassis_number': step2_data['chassis_number'],
                'or_number': step2_data['or_number'],
                'cr_number': step2_data['cr_number'],

                # Owner Information (if not the applicant)
                'owner_firstname': step2_data.get('owner_firstname', ''),
                'owner_middlename': step2_data.get('owner_middlename', ''),
                'owner_lastname': step2_data.get('owner_lastname', ''),
                'owner_suffix': step2_data.get('owner_suffix', ''),
                'relationship_to_owner': step2_data.get('relationship_to_owner', ''),
                'contact_number': step2_data.get('contact_number', ''),
                'address': step2_data.get('address', ''),
            }

            return redirect('vehicle_registration_step_3')
    else:
        form = VehicleRegistrationStep2Form()

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'Forms/forms_2.html', context)


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

                # Update UserProfile with collected information
                if step1_data.get('middlename'):
                    user.middlename = step1_data['middlename']
                if step1_data.get('address'):
                    user.address = step1_data['address']
                if step1_data.get('role'):
                    user.school_role = step1_data['role']
                if step1_data.get('department_or_workplace'):
                    user.department = step1_data['department_or_workplace']
                if step1_data.get('college'):
                    user.college = step1_data['college']
                if step1_data.get('program'):
                    user.program = step1_data['program']
                if step1_data.get('driver_license_number'):
                    user.dl_number = step1_data['driver_license_number']

                user.save()

                # Create Vehicle object
                vehicle = Vehicle.objects.create(
                    applicant=user,
                    make_model=step2_data['make_model'],
                    plate_number=step2_data['plate_number'],
                    year_model=step2_data['year_model'],
                    color=step2_data['color'],
                    type=step2_data['type'],
                    engine_number=step2_data['engine_number'],
                    chassis_number=step2_data['chassis_number'],
                    or_number=step2_data.get('or_number', ''),
                    cr_number=step2_data.get('cr_number', ''),
                    owner_firstname=None if step2_data.get('owner') == 'yes' else step2_data.get('owner_firstname'),
                    owner_middlename=None if step2_data.get('owner') == 'yes' else step2_data.get('owner_middlename'),
                    owner_lastname=None if step2_data.get('owner') == 'yes' else step2_data.get('owner_lastname'),
                    owner_suffix=None if step2_data.get('owner') == 'yes' else step2_data.get('owner_suffix'),
                    contact_number=None if step2_data.get('owner') == 'yes' else step2_data.get('contact_number'),
                    relationship_to_owner=None if step2_data.get('owner') == 'yes' else step2_data.get('relationship_to_owner'),
                    address=None if step2_data.get('owner') == 'yes' else step2_data.get('address'),
                )

                # Create Registration object
                Registration.objects.create(
                    user=user,
                    vehicle=vehicle,
                    files=google_folder_link,
                    status='application submitted'
                )

                # Clear session data
                for key in ['step1_data', 'step2_data']:
                    request.session.pop(key, None)

                messages.success(request, "Vehicle registration submitted successfully!")
                return redirect('user_pass_status')

            except Exception as e:
                messages.error(request, f"Error saving registration: {str(e)}")

        # If form is invalid or exception occurred, fall through to render again

    else:
        form = VehicleRegistrationStep3Form()

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'Forms/forms_3.html', context)



def registration_complete(request):
    return render(request, 'User Dashboard/User_Pass_Status')

@login_required
def user_pass_status(request):
    return render(request, "User Dashboard/User_Pass_Status.html")

@login_required
def user_settings(request):
    return render(request, "User Dashboard/User_Settings.html")

# Admin Page View

@login_required
def admin_dashboard(request):
    # Total users by role
    total_students = UserProfile.objects.filter(school_role='student').count()
    total_security = UserProfile.objects.filter(role='security').count()
    total_cashier = UserProfile.objects.filter(role='cashier').count()
    total_admin = UserProfile.objects.filter(role='admin').count()

    # Account growth calculation
    current_month_users = UserProfile.objects.filter(
        created_at__gte=now().replace(day=1)
    ).count()
    previous_month_users = UserProfile.objects.filter(
        created_at__lt=now().replace(day=1),
        created_at__gte=(now().replace(day=1) - timedelta(days=30))
    ).count()
    growth_percent = round(((current_month_users - previous_month_users) / previous_month_users) * 100, 1) if previous_month_users > 0 else 0

    # Monthly Registered Students
    monthly_users = (
        UserProfile.objects
        .filter(school_role='student')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    monthly_totals = {month: 0 for month in range(1, 13)}
    for entry in monthly_users:
        month_num = entry['month'].month
        monthly_totals[month_num] = entry['total']
    monthly_chart_data = list(monthly_totals.values())

    # Chart Data for Transactions by Status
    # chart_data = PaymentTransaction.objects.values('status').annotate(count=Count('id'))

    # Fetch all transactions for the table
    # transaction_list = PaymentTransaction.objects.select_related(
    #     'registration__user', 'cashier__user'
    # ).all().order_by('-date_processed')  # Order newest first (optional)

    context = {
        "total_students": total_students,
        "total_security": total_security,
        "total_cashier": total_cashier,
        "total_admin": total_admin,
        "growth_percent": growth_percent,
        "monthly_chart_data": monthly_chart_data,
        # "chart_data": chart_data,
        # "transaction_list": transaction_list,  # Add this for your table
    }

    return render(request, "Admin Dashboard/Admin_Dashboard.html", context)



class AdminViewUser(CustomLoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = "users"
    template_name = 'Admin Dashboard/Admin_Manage_User.html'
    paginate_by = 20

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
# class adminViewPayment(ListView):
#     model = PaymentTransaction
#     template_name = "Admin Dashboard/Admin_Manage_Payment.html"
#     context_object_name = 'payment_list'
#     paginate_by = 20

#     def get_queryset(self):
#         return PaymentTransaction.objects.filter(status='pending')
    
# class adminViewTransaction(ListView):
#     model = PaymentTransaction
#     template_name = "Admin Dashboard/Admin_Transaction.html"
#     context_object_name = 'transaction_list'
#     paginate_by = 20

#     def get_queryset(self):
#         return PaymentTransaction.objects.exclude(status='pending')
    
# class adminUpdatePayment(UpdateView):
#     model = PaymentTransaction
#     form_class = PaymentTransactionForm
#     template_name ="Admin Dashboard/Admin_Payment_Update.html"
#     success_url = reverse_lazy("admin_payments")

@login_required
def admin_manage_passes(request):
    vehicle_passes = VehiclePass.objects.select_related(
        'vehicle', 
        'vehicle__applicant',
    ).all()

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
    paginate_by = 20

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


# Cashier Page View @login_required
# @login_required
# def cashier_dashboard(request):
#     today = now().date()

#     # Total student accounts
#     total_accounts = UserProfile.objects.filter(school_role='student').count()

#     # Account growth: this month vs last month
#     current_month_start = now().replace(day=1)
#     last_month_start = (current_month_start - timedelta(days=30)).replace(day=1)

#     current_month_users = UserProfile.objects.filter(
#         created_at__gte=current_month_start,
#         school_role='student'
#     ).count()

#     last_month_users = UserProfile.objects.filter(
#         created_at__gte=last_month_start,
#         created_at__lt=current_month_start,
#         school_role='student'
#     ).count()

#     account_growth_percent = round(((current_month_users - last_month_users) / last_month_users) * 100, 1) if last_month_users else 0

#     # Pending payments (as of today)
#     pending_payments = PaymentTransaction.objects.filter(
#         status='pending', created_at__date=today
#     ).count()

#     # Total paid clients
#     paid_clients = PaymentTransaction.objects.filter(status='paid').values('registration__user').distinct().count()

#     # Paid clients by month (for chart)
#     paid_clients_monthly = (
#         PaymentTransaction.objects.filter(status='paid')
#         .annotate(month=TruncMonth('created_at'))
#         .values('month')
#         .annotate(total=Count('id'))
#         .order_by('month')
#     )

#     # Format for chart.js (ensure 12 months)
#     monthly_paid_totals = {month: 0 for month in range(1, 13)}
#     for entry in paid_clients_monthly:
#         if entry['month']:
#             month_number = entry['month'].month
#             monthly_paid_totals[month_number] = entry['total']
#     paid_clients_data = list(monthly_paid_totals.values())

#     # Payments table
#     payment_list = PaymentTransaction.objects.select_related(
#         'registration__user'
#     ).order_by('-created_at')[:20]

#     context = {
#         'total_accounts': total_accounts,
#         'account_growth_percent': account_growth_percent,
#         'pending_payments': pending_payments,
#         'paid_clients': paid_clients,
#         'paid_clients_data': paid_clients_data,
#         'payment_list': payment_list,
#         'current_date': today.strftime("%B %d, %Y")
#     }

#     return render(request, 'Cashier Dashboard/Cashier_Dashboard.html', context)

# class cashierViewPayment(CustomLoginRequiredMixin, ListView):
#     model = PaymentTransaction
#     template_name = "Cashier Dashboard/Cashier_Payment.html"
#     context_object_name = 'payment_list'
#     paginate_by = 20

#     def get_queryset(self):
#         return PaymentTransaction.objects.filter(status='pending')
    
# class cashierViewTransaction(CustomLoginRequiredMixin, ListView):
#     model = PaymentTransaction
#     template_name = "Cashier Dashboard/Cashier_Transaction.html"
#     context_object_name = 'transaction_list'
#     paginate_by = 20

#     def get_queryset(self):
#         return PaymentTransaction.objects.exclude(status='pending')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Get the user ID from the session
#         user_id = self.request.session.get('user_id')
        
#         # Get the actual UserProfile instance
#         if user_id:
#             user_profile = UserProfile.objects.get(id=user_id)
#             context['form'] = PaymentTransactionForm(user=user_profile)
#         else:
#             context['form'] = PaymentTransactionForm()
        
#         return context

# class cashierUpdatePayment(CustomLoginRequiredMixin, UpdateView):
#     model = PaymentTransaction
#     form_class = PaymentTransactionForm
#     template_name ="Cashier Dashboard/Cashier_Payment_Update.html"
#     success_url = reverse_lazy("cashier_payments")

# @login_required
# def cashier_report(request):
#     return render(request, "Cashier Dashboard/Cashier_Reports.html")

# Security Page Views
@login_required
def security_dashboard(request):
    return render(request, "Security Dashboard/security_dashboard.html")

@login_required
def security_manage_application(request):
    return render(request, "Security Dashboard/Security_Application.html")

class SecurityViewApplication(CustomLoginRequiredMixin, ListView):
    model = Registration
    template_name = 'Security Dashboard/Security_Application.html'
    context_object_name = 'applications'
    paginate_by = 20

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

# class SecurityViewInspectionReports(CustomLoginRequiredMixin, ListView):
#     model = InspectionReport
#     template_name = 'Security Dashboard/Security_Inspection.html'
#     context_object_name = 'inspections'
#     paginate_by = 20

#     def get_queryset(self):
#         return InspectionReport.objects.exclude(remarks='sticker_released')
    
# class SecurityUpdateFinalInspectionDate(CustomLoginRequiredMixin, UpdateView):
#     model = InspectionReport
#     form_class = FinalDateInspectionForm
#     template_name = 'Security Dashboard/Security Application CRUD/Security_Update_Final_Inspection_Date.html'
#     success_url = reverse_lazy('security_manage_inspection')

# def handle_inspection_action(request):
#     if request.method == "POST":
#         # Debug information
#         print("POST data received:", request.POST)
        
#         inspection_id = request.POST.get('inspection_id')
#         action = request.POST.get('action')
#         additional_notes = request.POST.get('additional_notes', '')
        
#         print(f"Extracted values - inspection_id: {inspection_id}, action: {action}, notes: {additional_notes}")
        
#         if inspection_id and action:
#             try:
#                 # Check that ID is valid before attempting to get object
#                 if not inspection_id.isdigit():
#                     messages.error(request, f"Invalid inspection ID format: {inspection_id}")
#                     return redirect('security_manage_inspection')
                
#                 inspection = InspectionReport.objects.get(id=inspection_id)
#                 inspection.additional_notes = additional_notes
                
#                 if action == 'approve':
#                     inspection.is_approved = True
#                     inspection.remarks = 'sticker released'
#                 elif action == 'reject':
#                     inspection.is_approved = False
#                     inspection.remarks = 'application declined'
#                 else:
#                     messages.error(request, f"Invalid action: {action}")
#                     return redirect('security_manage_inspection')
                    
#                 inspection.save()
#                 messages.success(request, f"Inspection {action}d successfully.")
#             except InspectionReport.DoesNotExist:
#                 messages.error(request, f"Inspection record not found for ID: {inspection_id}")
#             except Exception as e:
#                 messages.error(request, f"Error: {str(e)}")
#                 print(f"Exception details: {type(e).__name__}, {str(e)}")
#         else:
#             messages.error(request, f"Missing required parameters. Got inspection_id={inspection_id}, action={action}")
#     else:
#         messages.error(request, "This endpoint only accepts POST requests.")
    
#     return redirect('security_manage_inspection')

class SecurityViewStickers(CustomLoginRequiredMixin, ListView):
    model = VehiclePass
    template_name = 'Security Dashboard/Security_Release_Stickers.html'
    context_object_name = 'stickers'
    paginate_by = 20

@login_required
def security_report(request):
    return render(request, "Security Dashboard/Security_History.html")


@login_required
def settings_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to access settings.")
        return redirect('login')  # Replace with your login route name

    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        # Only allow if user is authenticated (should already be ensured by @login_required)
        if not request.user.is_authenticated:
            return redirect('login')  # or wherever your login page is

        # === Handle profile update ===
        corporate_email = request.POST.get('corporate_email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        middlename = request.POST.get('middlename')
        suffix = request.POST.get('suffix')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        user.corporate_email = corporate_email
        user.firstname = firstname
        user.lastname = lastname
        user.middlename = middlename
        user.suffix = suffix
        user.address = address

        if profile_picture:
            user.profile_picture = profile_picture

        # === Handle password update ===
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            if new_password == confirm_password:
                user.password = new_password  # Save securely if you hash it manually
                messages.success(request, "Password updated successfully.")
            else:
                messages.error(request, "Passwords do not match.")
                return redirect(request.path)
        
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect(request.path)

    # === GET Request ===
    context = {
        'user': user
    }

    # Role-specific template and context
    if user.role == 'admin':
        context['all_vehicles'] = Vehicle.objects.select_related('self_owner').all()
        template_name = 'Settings/admin_settings.html'
    elif user.role == 'cashier':
        template_name = 'Settings/cashier_settings.html'
    elif user.role == 'security':
        context['all_vehicles'] = Vehicle.objects.select_related('self_owner').all()
        template_name = 'Settings/security_settings.html'
    elif user.role == 'user':
        context['user_vehicle'] = Vehicle.objects.filter(applicant=user)
        template_name = 'Settings/user_settings.html'
    else:
        messages.error(request, "Unknown role. Contact admin.")
        return redirect('home')

    return render(request, template_name, context)

# def report_dashboard(request):
#     payments = PaymentTransaction.objects.select_related('registration__user')

#     # Filters
#     status_filter = request.GET.get('status')
#     deadline_filter = request.GET.get('nearing_deadline')

#     if status_filter:
#         payments = payments.filter(status=status_filter)

#     if deadline_filter == 'true':
#         payments = payments.filter(due_date__lte=now() + timedelta(days=3))

#     context = {
#         'payments_by_college': payments.values('registration__user__college').annotate(count=Count('id')).order_by('-count'),
#         'payments_by_program': payments.values('registration__user__program').annotate(count=Count('id')).order_by('-count'),
#         'payments_by_department': payments.values('registration__user__department').annotate(count=Count('id')).order_by('-count'),
#         'payments_by_school_role': payments.values('registration__user__school_role').annotate(count=Count('id')).order_by('-count'),
#         'payments_by_role': payments.values('registration__user__role').annotate(count=Count('id')).order_by('-count'),
#         'transactions_by_college': Registration.objects.values('user__college').annotate(count=Count('id')).order_by('-count'),
#         'transactions_by_program': Registration.objects.values('user__program').annotate(count=Count('id')).order_by('-count'),
#         'transactions_by_department': Registration.objects.values('user__department').annotate(count=Count('id')).order_by('-count'),
#         'transactions_by_school_role': Registration.objects.values('user__school_role').annotate(count=Count('id')).order_by('-count'),
#         'transactions_by_role': Registration.objects.values('user__role').annotate(count=Count('id')).order_by('-count'),
#         'filtered_payments': payments,
#     }
#     return render(request, 'report_dashboard.html', context)

def faq(request):
    return render(request, "Settings/FAQ.html")

def contact_us(request):
    return render(request, "Settings/ContactUs.html")

def about_us(request):
    return render(request, "Settings/AboutUs.html")

#Total Visitors
def get_stats():
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    total_visitors = SiteVisit.objects.count()
    weekly_visitors = SiteVisit.objects.filter(created_at__gte=week_ago).count()
    monthly_visitors = SiteVisit.objects.filter(created_at__gte=month_ago).count()

    total_logins = LoginActivity.objects.count()
    weekly_logins = LoginActivity.objects.filter(login_time__gte=week_ago).count()

    return {
        "total_visitors": total_visitors,
        "weekly_visitors": weekly_visitors,
        "monthly_visitors": monthly_visitors,
        "total_logins": total_logins,
        "weekly_logins": weekly_logins,
    }

def dashboard_view(request):
    stats = get_stats()
    return render(request, 'User Dashboard/User_Dashboard.html', {'stats': stats})


