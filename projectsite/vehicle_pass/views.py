from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import (CustomUser, UserProfile, SecurityProfile, CashierProfile, AdminProfile,
                     Vehicle, VehiclePass, Registration, RegistrationStatus, 
                     PaymentTransaction, InspectionReport, Notification, Announcement)
from django.contrib import messages

class UserRegistrationView(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        corporate_email = request.POST.get('corporate_email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if CustomUser.objects.filter(corporate_email=corporate_email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        user = CustomUser.objects.create_user(corporate_email=corporate_email, password=password, role=role)
        login(request, user)
        return redirect('dashboard')

@method_decorator(login_required, name='dispatch')
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})

class ProfileDetailView(View):
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'profile_detail.html', {'profile': profile})

class SecurityProfileDetailView(View):
    def get(self, request):
        profile = get_object_or_404(SecurityProfile, user=request.user)
        return render(request, 'security_profile.html', {'profile': profile})

class CashierProfileDetailView(View):
    def get(self, request):
        profile = get_object_or_404(CashierProfile, user=request.user)
        return render(request, 'cashier_profile.html', {'profile': profile})

class AdminProfileDetailView(View):
    def get(self, request):
        profile = get_object_or_404(AdminProfile, user=request.user)
        return render(request, 'admin_profile.html', {'profile': profile})

class ProfileUpdateView(View):
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'profile_update.html', {'profile': profile})
    
    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        profile.firstname = request.POST.get('firstname', profile.firstname)
        profile.lastname = request.POST.get('lastname', profile.lastname)
        profile.address = request.POST.get('address', profile.address)
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_detail')


@method_decorator(login_required, name='dispatch')
def register_vehicle(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'userprofile'):
            return JsonResponse({'error': 'User profile not found.'}, status=400)
        
        user_profile = request.user.userprofile
        if Vehicle.objects.filter(owner=user_profile).count() >= 2:
            return JsonResponse({'error': 'You can only register up to two vehicles.'}, status=400)

        vehicle = Vehicle.objects.create(
            owner=user_profile,
            plateNumber=request.POST.get('plateNumber'),
            type=request.POST.get('type'),
            model=request.POST.get('model'),
            color=request.POST.get('color'),
            chassisNumber=request.POST.get('chassisNumber'),
            OR_Number=request.POST.get('OR_Number')
        )
        return JsonResponse({'message': 'Vehicle registered successfully'})
    return render(request, 'register_vehicle.html')


@method_decorator(login_required, name='dispatch')
def submit_registration(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, id=request.POST.get('user_id'))
        vehicle = get_object_or_404(Vehicle, id=request.POST.get('vehicle_id'))
        
        registration = Registration.objects.create(
            applicationNumber=request.POST.get('applicationNumber'),
            user=user_profile,
            vehicle=vehicle,
            files=request.FILES.get('files')  # Handle file upload properly
        )
        return JsonResponse({'message': 'Registration submitted successfully'})
    return render(request, 'submit_registration.html')


@method_decorator(login_required, name='dispatch')
def update_registration_status(request):
    if request.method == 'POST':
        registration = get_object_or_404(Registration, id=request.POST.get('registration_id'))
        
        valid_statuses = ['Pending', 'Approved', 'Rejected']
        status = request.POST.get('status')

        if status not in valid_statuses:
            return JsonResponse({'error': 'Invalid status value.'}, status=400)

        registration.status = status 
        registration.save()

        RegistrationStatus.objects.create(
            registration=registration,
            remarks=request.POST.get('remarks', '')
        )

        return JsonResponse({'message': 'Registration status updated successfully'})
    return render(request, 'update_registration_status.html')


@method_decorator(login_required, name='dispatch')
def issue_vehicle_pass(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        pass_number = request.POST.get('passNumber')
        pass_expire = request.POST.get('passExpire')
        status = request.POST.get('status')
        
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        vehicle_pass = VehiclePass(
            vehicle=vehicle,
            passNumber=pass_number,
            passExpire=pass_expire,
            status=status
        )
        vehicle_pass.save()
        
        return JsonResponse({'message': 'Vehicle pass issued successfully'})
    return render(request, 'issue_vehicle_pass.html')


@method_decorator(login_required, name='dispatch')
class VehicleListView(View):
    def get(self, request):
        vehicles = Vehicle.objects.filter(owner=request.user.userprofile)
        return render(request, 'vehicles/list.html', {'vehicles': vehicles})

@method_decorator(login_required, name='dispatch')
class RegistrationListView(View):
    def get(self, request):
        registrations = Registration.objects.filter(user=request.user.userprofile)
        return render(request, 'registrations/list.html', {'registrations': registrations})

@method_decorator(login_required, name='dispatch')
class PaymentTransactionListView(View):
    def get(self, request):
        transactions = PaymentTransaction.objects.filter(registration__user=request.user.userprofile)
        return render(request, 'payments/list.html', {'transactions': transactions})

@method_decorator(login_required, name='dispatch')
class InspectionReportListView(View):
    def get(self, request):
        reports = InspectionReport.objects.all()
        return render(request, 'inspections/list.html', {'reports': reports})

@method_decorator(login_required, name='dispatch')
class NotificationListView(View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        return render(request, 'notifications/list.html', {'notifications': notifications})

@method_decorator(login_required, name='dispatch')
class AnnouncementListView(View):
    def get(self, request):
        announcements = Announcement.objects.all().order_by('-date_posted')
        return render(request, 'announcements/list.html', {'announcements': announcements})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
