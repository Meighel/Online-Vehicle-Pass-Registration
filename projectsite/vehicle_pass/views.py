from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserSignupForm, UserProfileForm, RegistrationForm, PasswordUpdateForm, VehicleRegistrationStep1Form, VehicleRegistrationStep2Form, VehicleRegistrationStep3Form, OICRecommendForm, DirectorApproveForm
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
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import timedelta 
import pytz
import csv

from django.db.models import Count, Q
from django.utils.timezone import now
import calendar
from django.db.models.functions import TruncMonth
from django.contrib.auth import update_session_auth_hash
from .models import SiteVisit, LoginActivity

import os
import csv
import pytz

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

# imports for notification
from django.core.paginator import Paginator
from .notification_utils import (
    get_user_notifications,
    mark_all_notifications_read,
    create_announcement_notification
)
import json

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
            # 🔑 Important fixes
            request.session.flush()               # clear any old session
            request.session["user_id"] = user.id  # set current user
            request.session.cycle_key()           # rotate session key (security)
            
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

    context = {
        'profile': profile,
        'registration': registration,
        'history': history,
    }

    return render(request, "User/User_Dashboard.html", context)

@login_required
def user_application(request):
    return render(request, "User/User_Application.html")

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
                'dl_number': step1_data['dl_number'],
                'contact': step1_data['contact'],
                'corporate_email': step1_data['corporate_email'],
                'school_role': step1_data['school_role'],

                # Employees
                'position': step1_data['position'],
                'workplace': step1_data['workplace'],

                # Students
                'college': step1_data['college'],
                'program': step1_data['program'],
                'year_level': step1_data['year_level'],

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
            'lastname': user.lastname,
            'firstname': user.firstname,
            'middlename': user.middlename,
            'suffix': user.suffix,
            'address': user.address,
            'dl_number': user.dl_number,
            'contact': user.contact,
            'corporate_email': user.corporate_email,
            'school_role': user.school_role,
            
            #employees
            'position': getattr(user, 'position', ''),
            'workplace': getattr(user, 'workplace', ''),
            
            #student
            'college': getattr(user, 'college', ''), 
            'program': getattr(user, 'program', ''),
            'year_level': getattr(user, 'year_level', ''),
            
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

@login_required
def vehicle_registration_step_2(request):
    user_id = request.session.get("user_id")
    user = UserProfile.objects.get(id=user_id)

    if 'step1_data' not in request.session:
        messages.error(request, "Please complete the form step by step.")
        return redirect('vehicle_registration_step_1')

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
                'is_owner': True if step2_data['owner'] == 'yes' else False,

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
        if 'step1_data' not in request.session:
            messages.error(request, "Please complete the form step by step.")
            return redirect('vehicle_registration_step_1')
        
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

    # --- ADD THESE CHECKS ---
    # Ensure step 1 data exists
    if 'step1_data' not in request.session:
        messages.error(request, "Please complete Step 1 first.")
        return redirect('vehicle_registration_step_1')
    # Ensure step 2 data exists
    if 'step2_data' not in request.session:
        messages.error(request, "Please complete Step 2 first.")
        return redirect('vehicle_registration_step_2')
    # --------------------------

    if request.method == 'POST':
        form = VehicleRegistrationStep3Form(request.POST, request.FILES)
        if form.is_valid():
            google_folder_link = form.cleaned_data['google_drive_link']
            printed_name = form.cleaned_data['printed_name']
            e_signature = form.cleaned_data['e_signature']


            try:
                # Get data from previous steps
                step1_data = request.session.get('step1_data', {})
                step2_data = request.session.get('step2_data', {})

                # Update UserProfile
                if step1_data.get('firstname'):
                    user.firstname = step1_data['firstname']
                if step1_data.get('middlename'):
                    user.middlename = step1_data['middlename']
                if step1_data.get('lastname'):
                    user.lastname = step1_data['lastname']   
                if step1_data.get('suffix'):
                    user.suffix = step1_data['suffix'] 
                if step1_data.get('address'):
                    user.address = step1_data['address']
                if step1_data.get('dl_number'):
                    user.dl_number = step1_data['dl_number']
                if step1_data.get('contact'):
                    user.contact = step1_data['contact']
                if step1_data.get('corporate_email'):
                    user.corporate_email = step1_data['corporate_email']         
                if step1_data.get('school_role'):
                    user.school_role = step1_data['school_role']
                
                # employees
                if step1_data.get('position'):
                    user.position = step1_data['position']
                if step1_data.get('workplace'):
                    user.workplace = step1_data['workplace']
                    
                #student
                if step1_data.get('college'):
                    user.college = step1_data['college']
                if step1_data.get('program'):
                    user.program = step1_data['program']
                if step1_data.get('year_level'):
                    user.year_level = step1_data['year_level']
                    
                for field in ['father_name','father_contact','father_address',
                            'mother_name','mother_contact','mother_address',
                            'guardian_name','guardian_contact','guardian_address']:
                    if step1_data.get(field):
                        setattr(user, field, step1_data[field])
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
                    or_number=step2_data['or_number'],
                    cr_number=step2_data['cr_number'],
                    
                    # Owner fields:
                    owner_firstname=None if step2_data.get('is_owner', False) else step2_data.get('owner_firstname') or None,
                    owner_middlename=None if step2_data.get('is_owner', False) else step2_data.get('owner_middlename') or None,
                    owner_lastname=None if step2_data.get('is_owner', False) else step2_data.get('owner_lastname') or None,
                    owner_suffix=None if step2_data.get('is_owner', False) else step2_data.get('owner_suffix') or None,
                    relationship_to_owner=None if step2_data.get('is_owner', False) else step2_data.get('relationship_to_owner') or None,
                    contact_number=None if step2_data.get('is_owner', False) else step2_data.get('contact_number') or None,
                    address=None if step2_data.get('is_owner', False) else step2_data.get('address') or None,
                )

                # Create Registration object
                Registration.objects.create(
                    user=user,
                    vehicle=vehicle,
                    files=google_folder_link,
                    printed_name=printed_name,
                    e_signature=e_signature,
                    signature_date=timezone.now(),
                    status='pending'
                )

                # Clear session data
                request.session.pop('step1_data', None)
                request.session.pop('step2_data', None)

                messages.success(request, "Vehicle registration submitted successfully!")
                return redirect('user_pass_status')

            except Exception as e:
                import traceback
                print("DEBUG ERROR:", traceback.format_exc())  # logs full error in console
                messages.error(request, f"Error saving registration: {str(e)}")
        # If form is invalid or exception occurred, fall through to render again

    else:
        if 'step1_data' not in request.session:
            messages.error(request, "Please complete Step 1 first.")
            return redirect('vehicle_registration_step_1')
        if 'step2_data' not in request.session:
            messages.error(request, "Please complete Step 2 first.")
            return redirect('vehicle_registration_step_2')
        
        
        form = VehicleRegistrationStep3Form()

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'Forms/forms_3.html', context)


def registration_complete(request):
    return render(request, 'User/User_Pass_Status.html')

@login_required
def user_pass_status(request):
    return render(request, "User/User_Pass_Status.html")

@login_required
def user_settings(request):
    return render(request, "User/User_Settings.html")

# Admin Page View

@login_required
def admin_dashboard(request):
    # Total users by role
    total_students = UserProfile.objects.filter(school_role='student').count()
    total_officials = UserProfile.objects.filter(role='user', school_role__in=['faculty & staff', 'university official']).count()
    total_security = UserProfile.objects.filter(role='security').count()
    total_admin = UserProfile.objects.filter(role='admin').count()
    total_vehicles = Vehicle.objects.count() 
    total_motor = Vehicle.objects.filter(type='motor').count()
    total_car = Vehicle.objects.filter(type='car').count()
    total_van = Vehicle.objects.filter(type='van').count()

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

    context = {
        "total_students": total_students,
        "total_officials": total_officials,
        "total_security": total_security,
        "total_admin": total_admin,
        "growth_percent": growth_percent,
        "monthly_chart_data": monthly_chart_data,
        "total_vehicles": total_vehicles,
        'total_motor': total_motor,
        'total_car': total_car,
        'total_van': total_van,
    }

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    admin_profile = get_object_or_404(AdminProfile, user__id=user_id)
    user_profile = UserProfile.objects.filter(id=user_id).first()
    if user_profile:
        context['profile'] = user_profile

    return render(request, "Admin/Admin_Dashboard.html", context)

class AdminViewUser(CustomLoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = "users"
    template_name = 'Admin/Admin_Manage_User.html'
    paginate_by = 20

class AdminCreateUser(CustomLoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "Admin/Admin User CRUD/Admin_Create_User.html" 
    success_url  = reverse_lazy("admin_manage_user")
    
class AdminUpdateUser(CustomLoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "Admin/Admin User CRUD/Admin_Update_User.html"
    success_url  = reverse_lazy("admin_manage_user")
    
class AdminDeleteUser(CustomLoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = "Admin/Admin User CRUD/Admin_Delete_User.html"
    success_url = reverse_lazy('admin_manage_user')

    def form_valid(self, form):
        messages.success(self.request, 'Deleted successfully. ')
        return super().form_valid(form)

class AdminViewSpecificUser(CustomLoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'Admin/Admin User CRUD/Admin_View_Specific_User.html'
    context_object_name = 'user'
    

@login_required
def admin_manage_application(request):
    return render(request, "Admin/Admin_Application.html")

@login_required
def admin_manage_passes(request):
    vehicle_passes = VehiclePass.objects.select_related(
        'vehicle', 
        'vehicle__applicant',
    ).all()

    context = {
        'vehicle_passes': vehicle_passes,
    }
    return render(request, "Admin/Admin_Manage_Passes.html", context)


@login_required
def get_filtered_registrations(request):
    """
    Helper function to get the base queryset based on URL filters including time and status.
    Used by both report views and the CSV download function.
    """
    report_type = request.GET.get('report_type', 'status_summary')
    status_filter = request.GET.get('status', 'completed')
    nearing_deadline = request.GET.get('nearing_deadline') == 'true'
    report_year = request.GET.get('year')
    report_semester = request.GET.get('semester')
    
    base_queryset = Registration.objects.exclude(status='no application')
    
    # --- 1. Apply Status/Deadline Filters (For status_summary reports) ---
    if report_type == 'status_summary':
        if status_filter == 'pending':
            base_queryset = base_queryset.filter(
                status__in=['application submitted', 'initial approval', 'final approval']
            )
        elif status_filter == 'completed':
            base_queryset = base_queryset.filter(
                status__in=['approved', 'sticker released']
            )
            
        if nearing_deadline and status_filter == 'pending':
            five_days_ago = now() - timedelta(days=5)
            three_days_ago = now() - timedelta(days=3)
            
            base_queryset = base_queryset.filter(
                status='initial approval',
                created_at__lte=five_days_ago, 
                created_at__gt=three_days_ago
            )

    # --- 2. Apply Date Filters (For annual/semester reports) ---
    if report_year:
        try:
            year = int(report_year)
            start_date = timezone.datetime(year, 1, 1).replace(tzinfo=pytz.utc)
            end_date = timezone.datetime(year + 1, 1, 1).replace(tzinfo=pytz.utc)

            if report_type == 'semester' and report_semester:
                semester = int(report_semester)
                if semester == 1:
                    start_date = timezone.datetime(year, 1, 1).replace(tzinfo=pytz.utc)
                    end_date = timezone.datetime(year, 7, 1).replace(tzinfo=pytz.utc)
                elif semester == 2:
                    start_date = timezone.datetime(year, 7, 1).replace(tzinfo=pytz.utc)
                    end_date = timezone.datetime(year + 1, 1, 1).replace(tzinfo=pytz.utc)
            
            base_queryset = base_queryset.filter(date_of_filing__gte=start_date, date_of_filing__lt=end_date)
            
        except ValueError:
            pass

    # Ensure we only consider successfully completed transactions for date-based reports
    if report_type in ['annual', 'semester']:
        base_queryset = base_queryset.filter(status__in=['approved', 'sticker released'])
        
    # Pre-fetch related data for efficient reporting
    base_queryset = base_queryset.select_related('user', 'vehicle')
    
    return base_queryset


@login_required
def get_report_aggregates(request):
    """
    Helper to calculate the aggregation counts for the on-screen report cards.
    """
    base_queryset = get_filtered_registrations(request)
    
    reports = {
        'registrations_by_college': base_queryset.exclude(user__college__isnull=True).exclude(user__college='').values('user__college').annotate(count=Count('registration_number')).order_by('-count'),
        'registrations_by_program': base_queryset.exclude(user__program__isnull=True).exclude(user__program='').values('user__program').annotate(count=Count('registration_number')).order_by('-count'),
        'registrations_by_workplace': base_queryset.exclude(user__workplace__isnull=True).exclude(user__workplace='').values('user__workplace').annotate(count=Count('registration_number')).order_by('-count'),
        'registrations_by_school_role': base_queryset.exclude(user__school_role__isnull=True).exclude(user__school_role='').values('user__school_role').annotate(count=Count('registration_number')).order_by('-count'),
        'registrations_by_system_role': base_queryset.values('user__role').annotate(count=Count('registration_number')).order_by('-count'),
    }
    return reports


@login_required
def admin_report(request):
    """
    Generates and displays various reports based on Registration data.
    """
    reports = get_report_aggregates(request)

    context = {
        'report_type': request.GET.get('report_type', 'status_summary'),
        'status_filter': request.GET.get('status', 'completed'),
        'nearing_deadline': request.GET.get('nearing_deadline') == 'true',
        'report_year': request.GET.get('year'),
        'report_semester': request.GET.get('semester'),

        'registrations_by_college': reports['registrations_by_college'],
        'registrations_by_program': reports['registrations_by_program'],
        'registrations_by_workplace': reports['registrations_by_workplace'], 
        'registrations_by_school_role': reports['registrations_by_school_role'],
        'registrations_by_system_role': reports['registrations_by_system_role'],
    }

    return context

@login_required
def download_reports_csv(request):
    """
    Generates a CSV file for filtered registration records with columns specific
    to the chosen report type. Payment reports have a concise structure.
    """
    # Authorization Check (Keep the corrected version from previous step)
    user_id = request.session.get("user_id")
    if not user_id:
        return HttpResponseRedirect(reverse('login'))
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        if user_profile.role not in ['admin', 'security']:
            messages.error(request, "Permission denied.")
            return redirect('default_dashboard' if user_profile.role == 'user' else 'login')
    except UserProfile.DoesNotExist:
        request.session.flush()
        return HttpResponseRedirect(reverse('login'))

    # Get filtered data using the existing helper function
    registrations = get_filtered_registrations(request)
    report_type = request.GET.get('report_type', 'status_summary')

    response = HttpResponse(content_type='text/csv')
    filename = f"vehicle_registrations_{report_type}_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # --- Define Report Structure based on report_type ---

    # Helper for common fields (Used by Transaction & Default reports)
    def get_common_trans_fields(reg):
        return [
            reg.registration_number,
            reg.status.title(),
            reg.date_of_filing.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M"),
            f"{reg.user.firstname} {reg.user.lastname}",
        ]

    # --- Payment Reports (Concise Columns) ---
    if report_type.startswith('payment_') and report_type != 'payment_deadline':
        # Define base payment columns
        header = ['Registration ID', 'Applicant Name', 'Date Filed', 'Status']
        # Add the specific grouping column header based on report_type
        if 'college' in report_type: header.append('College')
        elif 'program' in report_type: header.append('Program')
        elif 'department' in report_type: header.append('Department/Workplace')
        elif 'personnel' in report_type or 'faculty' in report_type: header.append('Institutional Role')
        elif 'role' in report_type: header.append('System Role')

        # Define the data mapping function for payment reports
        def payment_mapper(reg):
            base_data = [
                reg.registration_number,
                f"{reg.user.firstname} {reg.user.lastname}",
                reg.date_of_filing.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M"),
                reg.status.title(),
            ]
            # Add the specific grouping data
            if 'college' in report_type: base_data.append(reg.user.college or 'N/A')
            elif 'program' in report_type: base_data.append(reg.user.program or 'N/A')
            elif 'department' in report_type: base_data.append(reg.user.workplace or 'N/A')
            elif 'personnel' in report_type or 'faculty' in report_type: base_data.append((reg.user.school_role or 'N/A').title())
            elif 'role' in report_type: base_data.append(reg.user.role.title())
            return base_data
        data_mapper = payment_mapper

    # --- Transaction Reports (Slightly more detail than Payment) ---
    elif report_type.startswith('trans_'):
        # Base transaction columns
        header = ['Registration ID', 'Status', 'Date Filed', 'Applicant Name']
        # Add grouping and vehicle columns
        if 'college' in report_type: header.extend(['College', 'Program'])
        elif 'program' in report_type: header.extend(['College', 'Program'])
        elif 'department' in report_type: header.extend(['Department/Workplace', 'Institutional Role'])
        elif 'personnel' in report_type or 'faculty' in report_type: header.extend(['Department/Workplace', 'Institutional Role'])
        elif 'role' in report_type: header.extend(['System Role', 'Institutional Role'])
        header.extend(['Vehicle Type', 'Plate Number']) # Common vehicle info for transactions

        # Define the data mapping function for transaction reports
        def transaction_mapper(reg):
            base_data = get_common_trans_fields(reg)
            # Add grouping data
            if 'college' in report_type: base_data.extend([reg.user.college or 'N/A', reg.user.program or 'N/A'])
            elif 'program' in report_type: base_data.extend([reg.user.college or 'N/A', reg.user.program or 'N/A'])
            elif 'department' in report_type: base_data.extend([reg.user.workplace or 'N/A', (reg.user.school_role or 'N/A').title()])
            elif 'personnel' in report_type or 'faculty' in report_type: base_data.extend([reg.user.workplace or 'N/A', (reg.user.school_role or 'N/A').title()])
            elif 'role' in report_type: base_data.extend([reg.user.role.title(), (reg.user.school_role or 'N/A').title()])
            # Add vehicle data
            base_data.extend([reg.vehicle.type.title(), reg.vehicle.plate_number])
            return base_data
        data_mapper = transaction_mapper

    # --- Default/Comprehensive (Status Summary, Annual, Semester, Deadline) ---
    else:
        header = [
            'Registration ID', 'Status', 'Date Filed', 'Applicant Last Name', 'Applicant First Name',
            'Applicant Email', 'Institutional Role', 'College/Workplace', 'Vehicle Type', 'Plate Number',
            'Initial Approved By', 'Final Approved By', 'Remarks'
        ]
        data_mapper = lambda reg: [
            reg.registration_number,
            reg.status.title(),
            reg.date_of_filing.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M"),
            reg.user.lastname,
            reg.user.firstname,
            reg.user.corporate_email,
            (reg.user.school_role or 'N/A').title(),
            reg.user.college if reg.user.college else reg.user.workplace or 'N/A',
            reg.vehicle.type.title(),
            reg.vehicle.plate_number,
            f"{reg.initial_approved_by.user.firstname} {reg.initial_approved_by.user.lastname}" if reg.initial_approved_by else '',
            f"{reg.final_approved_by.user.firstname} {reg.final_approved_by.user.lastname}" if reg.final_approved_by else '', # Corrected access
            reg.remarks if reg.remarks else ''
        ]

    # --- Write CSV ---
    writer.writerow(header)

    for reg in registrations:
        try:
             writer.writerow(data_mapper(reg))
        except Exception as e:
             print(f"Error writing row for registration {reg.registration_number}: {e}")
             writer.writerow([reg.registration_number, "Error writing row", str(e)] + [''] * (len(header) - 3))

    return response

class AdminViewApplication(CustomLoginRequiredMixin, ListView):
    model = Registration
    template_name = 'Admin/Admin_Application.html'
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
    template_name = 'Admin/Admin Application CRUD/Admin_View_Specific_Application.html'
    context_object_name = 'applications'

class AdminUpdateApplication(CustomLoginRequiredMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'Admin/Admin Application CRUD/Admin_Update_Application.html'
    success_url = reverse_lazy('admin_manage_application')

# Security Page Views
@login_required
def security_dashboard(request):
    # Fetch statistics
    verified_count = Registration.objects.filter(status='approved').count()
    rejected_count = Registration.objects.filter(status='rejected').count()
    total_count = Registration.objects.exclude(status='no application').count()
    percentage = round((verified_count / total_count * 100) if total_count else 0, 2)

    unreleased_stickers = Registration.objects.filter(
        status__in=['approved', 'final approval'],
        sticker_released_date__isnull=True
    ).select_related('user').order_by('-created_at')

    context = {
        'verified_count': verified_count,
        'rejected_count': rejected_count,
        'total_count': total_count,
        'percentage': percentage,
        'unreleased_stickers': unreleased_stickers,
    }
    return render(request, 'Security/security_dashboard.html', context)

@login_required
def security_manage_application(request):
    applications = Registration.objects.select_related('user', 'initial_approved_by', 'final_approved_by').all().order_by('-created_at')
    context = {
        'applications': applications,
    }
    return render(request, "Security/Security_Application.html")

class OICRequiredMixin:
    """
    Verify that the current user is an OIC.
    This runs *after* CustomLoginRequiredMixin.
    """
    def dispatch(self, request, *args, **kwargs):
        # We can assume user_id exists because CustomLoginRequiredMixin already checked it
        user_id = request.session.get("user_id") 
        
        try:
            # Get the security profile linked to the logged-in user
            security_profile = SecurityProfile.objects.get(user__id=user_id)
        except SecurityProfile.DoesNotExist:
            # User is logged in, but is not a security officer at all
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('default_dashboard') # Send them to their own dashboard

        # The actual role check
        if security_profile.level != 'oic':
            messages.error(request, "Only the OIC can perform this action.")
            return redirect('security_manage_application') # Send back to list
        
        # If check passes, continue to the view
        return super().dispatch(request, *args, **kwargs)

class DirectorRequiredMixin:
    """
    Verify that the current user is a Director.
    This runs *after* CustomLoginRequiredMixin.
    """
    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get("user_id")
        
        try:
            security_profile = SecurityProfile.objects.get(user__id=user_id)
        except SecurityProfile.DoesNotExist:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('default_dashboard')

        # The actual role check
        if security_profile.level != 'director':
            messages.error(request, "Only the GSO Director can perform this action.")
            return redirect('security_manage_application')
            
        # If check passes, continue to the view
        return super().dispatch(request, *args, **kwargs)

class SecurityViewApplication(CustomLoginRequiredMixin, ListView):
    model = Registration
    template_name = 'Security/Security_Application.html'
    context_object_name = 'applications'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oic_form'] = OICRecommendForm()
        context['director_form'] = DirectorApproveForm()
        return context

class SecurityViewSpecificApplication(CustomLoginRequiredMixin, DetailView):
    model = Registration
    template_name = 'Security/Security Application CRUD/Security_View_Specific_Application.html'
    context_object_name = 'registration'

# class SecurityUpdateApplication(CustomLoginRequiredMixin, UpdateView):
#     model = Registration
#     form_class = RegistrationForm
#     template_name = 'Security/Security Application CRUD/Security_Update_Application.html'
#     success_url = reverse_lazy('security_manage_application')

class SecurityRecommendView(CustomLoginRequiredMixin, OICRequiredMixin, UpdateView):
    """
    View for the OIC to recommend or reject an application.
    Checks: 1. Logged in (CustomLogin) 2. Is OIC (OICRequired)
    """
    model = Registration
    form_class = OICRecommendForm
    template_name = 'Security/Security_Application.html' # On error, re-renders the list
    success_url = reverse_lazy('security_manage_application')

    def get_object(self, queryset=None):
        # Only allow updates on applications in the correct state
        obj = super().get_object(queryset)
        if obj.status != 'application submitted':
            messages.error(self.request, "This application is not ready for recommendation.")
            return None 
        return obj

    def form_valid(self, form):
        messages.success(self.request, f"Application for {self.object.user.get_full_name()} has been updated.")
        # Set the approver to the current user's security profile
        form.instance.initial_approved_by = self.request.user_profile.securityprofile
        return super().form_valid(form)

class SecurityApproveView(CustomLoginRequiredMixin, DirectorRequiredMixin, UpdateView):
    """
    View for the Director to give final approval or reject.
    Checks: 1. Logged in (CustomLogin) 2. Is Director (DirectorRequired)
    """
    model = Registration
    form_class = DirectorApproveForm
    template_name = 'Security/Security_Application.html' # On error, re-renders the list
    success_url = reverse_lazy('security_manage_application')

    def get_object(self, queryset=None):
        # Only allow updates on applications in the correct state
        obj = super().get_object(queryset)
        if obj.status != 'initial approval':
            messages.error(self.request, "This application is not ready for final approval.")
            return None
        return obj

    def form_valid(self, form):
        messages.success(self.request, f"Application for {self.object.user.get_full_name()} has been approved.")
        # Set the final approver to the current user's security profile
        form.instance.final_approved_by = self.request.user_profile.securityprofile
        return super().form_valid(form)

@login_required
def security_release_stickers(request):
    stickers = VehiclePass.objects.select_related('vehicle__applicant').all().order_by('-created_at')
    return render(request, 'Security/Security_Release_Stickers.html', {'stickers': stickers})

@login_required
def security_report(request):
    """
    Generates and displays various reports based on Registration data for Security role.
    """
    reports = get_report_aggregates(request)

    context = {
        'report_type': request.GET.get('report_type', 'status_summary'),
        'status_filter': request.GET.get('status', 'completed'),
        'nearing_deadline': request.GET.get('nearing_deadline') == 'true',
        'report_year': request.GET.get('year'),
        'report_semester': request.GET.get('semester'),
        
        'registrations_by_college': reports['registrations_by_college'],
        'registrations_by_program': reports['registrations_by_program'],
        'registrations_by_workplace': reports['registrations_by_workplace'], 
        'registrations_by_school_role': reports['registrations_by_school_role'],
        'registrations_by_system_role': reports['registrations_by_system_role'],
    }

    return render(request, "Security/Security_Reports.html", context)

@login_required
def settings_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to access settings.")
        return redirect('login')  # Replace with your login route name

    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        # === Handle profile update (corporate_email and role are immutable) ===
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        middlename = request.POST.get('middlename')
        suffix = request.POST.get('suffix')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        dl_number = request.POST.get('dl_number')
        school_role = request.POST.get('school_role') or None
        college = request.POST.get('college') or None
        program = request.POST.get('program') or None

        if firstname is not None:
            user.firstname = firstname
        if lastname is not None:
            user.lastname = lastname
        if middlename is not None:
            user.middlename = middlename
        if suffix is not None:
            user.suffix = suffix
        if address is not None:
            user.address = address
        if contact is not None:
            user.contact = contact
        if dl_number is not None:
            user.dl_number = dl_number
        if school_role in ['student', 'faculty & staff', 'university official', None, '']:
            user.school_role = school_role or None
        if college is not None:
            user.college = college
        if program is not None:
            user.program = program

        # === Handle password update ===
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password or confirm_password:
            if new_password and confirm_password and new_password == confirm_password:
                user.password = new_password
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
        context['all_vehicles'] = Vehicle.objects.select_related('applicant').all()
        template_name = 'Settings/admin_settings.html'
    elif user.role == 'security':
        context['all_vehicles'] = Vehicle.objects.select_related('applicant').all()
        template_name = 'Settings/security_settings.html'
    elif user.role == 'user':
        context['user_vehicle'] = Vehicle.objects.filter(applicant=user)
        template_name = 'Settings/user_settings.html'
    else:
        messages.error(request, "Unknown role. Contact admin.")
        return redirect('home')

    return render(request, template_name, context)

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

def initials_avatar(request):
    user = request.user
    initials = ""
    if hasattr(user, "firstname") and user.firstname:
        initials += user.firstname[0].upper()
    if hasattr(user, "lastname") and user.lastname:
        initials += user.lastname[0].upper()
    if not initials:
        initials = "U"
    # Cache path
    cache_dir = os.path.join(settings.MEDIA_ROOT, "avatars")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"avatar_{user.id}.png")
    if not os.path.exists(cache_path):
        # Create image
        img_size = (80, 80)
        img = Image.new("RGB", img_size, color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        font_path = os.path.join(settings.BASE_DIR, "arial.ttf") # Use a valid font path
        try:
            font = ImageFont.truetype(font_path, 36)
        except:
            font = ImageFont.load_default()
        w, h = draw.textsize(initials, font=font)
        draw.text(((img_size[0]-w)/2, (img_size[1]-h)/2), initials, font=font, fill=(255, 215, 0))
        img.save(cache_path)
    with open(cache_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")
    
@login_required
def get_notifications_api(request):
    """API endpoint to get user notifications via AJAX"""
    user_id = request.session.get("user_id")
    user = get_object_or_404(UserProfile, id=user_id)
    
    # Parameters
    page = int(request.GET.get('page', 1))
    unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
    limit = int(request.GET.get('limit', 10))
    
    # Get notifications
    notifications_qs = get_user_notifications(user, unread_only=unread_only)
    
    # Paginate
    paginator = Paginator(notifications_qs, limit)
    page_obj = paginator.get_page(page)
    
    # Serialize notifications
    notifications_data = []
    for notification in page_obj:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'is_read': notification.is_read,
            'action_url': notification.action_url,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_ago': get_time_ago(notification.created_at)
        })
    
    # Get unread count
    unread_count = Notification.objects.filter(
        recipient=user,
        is_read=False
    ).count()
    
    return JsonResponse({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    })

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_notification_read_api(request, notification_id):
    """Mark a specific notification as read"""
    user_id = request.session.get("user_id")
    user = get_object_or_404(UserProfile, id=user_id)
    
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=user
        )
        notification.mark_as_read()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification marked as read'
        })
        
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found'
        }, status=404)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_all_read_api(request):
    """Mark all notifications as read"""
    user_id = request.session.get("user_id")
    user = get_object_or_404(UserProfile, id=user_id)
    
    count = mark_all_notifications_read(user)
    
    return JsonResponse({
        'success': True,
        'message': f'Marked {count} notifications as read',
        'updated_count': count
    })

@login_required
def get_unread_count_api(request):
    """Get just the unread notification count"""
    user_id = request.session.get("user_id")
    user = get_object_or_404(UserProfile, id=user_id)
    
    unread_count = Notification.objects.filter(
        recipient=user,
        is_read=False
    ).count()
    
    return JsonResponse({
        'unread_count': unread_count
    })

def get_time_ago(datetime_obj):
    """Helper function to get human readable time difference"""
    from django.utils import timezone
    import math
    
    now = timezone.now()
    diff = now - datetime_obj
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = math.floor(diff.seconds / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = math.floor(diff.seconds / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

# Admin/Security views for creating announcements
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_announcement_api(request):
    """API to create announcements (admin/security only)"""
    user_id = request.session.get("user_id")
    user = get_object_or_404(UserProfile, id=user_id)
    
    # Check if user has permission (admin or security)
    if not (user.role in ['admin', 'security']):
        return JsonResponse({
            'success': False,
            'message': 'Permission denied'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        
        announcement = Announcement.objects.create(
            title=data['title'],
            message=data['message'],
            posted_by=user,
            send_to_all=data.get('send_to_all', True),
            target_roles=data.get('target_roles', []),
            send_email=data.get('send_email', False)
        )
        
        # Create notifications
        notifications = create_announcement_notification(announcement)
        
        return JsonResponse({
            'success': True,
            'message': f'Announcement created and sent to {len(notifications)} users',
            'announcement_id': announcement.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating announcement: {str(e)}'
        }, status=400)