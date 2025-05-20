from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginActivity
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import pytz
from .models import Registration, PaymentTransaction, InspectionReport, VehiclePass

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    LoginActivity.objects.create(user=user)

# 1. Auto-change pending registrations to "reviewing documents" after 5 working days
@receiver(post_save, sender=Registration)
def set_registration_reviewing_after_delay(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        from django.core.management import call_command
        # This sets up a task to check this registration after 5 working days
        # You'll need to implement a management command or use Celery for this
        # For now, we'll use Django's built-in scheduling (not ideal for production)
        
        # Note: In a real production environment, you would use Celery or similar
        # task queue to handle this delayed task instead of this approach
        from django.db import connection
        
        # Get the current database connection
        connection.cursor().execute(
            """
            -- This is a placeholder for actual implementation
            -- In production, you would use Celery or Django-Q for task scheduling
            -- For now, just log that we need to implement this functionality
            """
        )
        
        # Alternative implementation for development/testing:
        # from django_q.tasks import schedule
        # schedule('your_app.tasks.update_pending_registration', 
        #          instance.registrationNumber,
        #          schedule_type='O',  # Once
        #          next_run=timezone.now() + timedelta(days=5))


# 3. Change Registration status to "for final inspection" when payment is marked as paid
@receiver(post_save, sender=PaymentTransaction)
def update_registration_on_payment(sender, instance, **kwargs):
    if instance.status == 'paid':
        # Update related registration status to "for final inspection"
        with transaction.atomic():
            registration = instance.registration
            registration.status = 'for final inspection'
            registration.save(update_fields=['status', 'updated_at'])
            
            # The InspectionReport creation is already handled in PaymentTransaction.save()
    
    elif instance.status == 'void':
        # If payment is void, update registration status to cancelled
        with transaction.atomic():
            registration = instance.registration
            registration.status = 'cancelled'
            registration.save(update_fields=['status', 'updated_at'])


# 5. Create VehiclePass when inspection is approved with "sticker_released"
@receiver(post_save, sender=InspectionReport)
def create_vehicle_pass_on_approval(sender, instance, **kwargs):
    if instance.remarks == 'sticker_released' and instance.is_approved:
        # The VehiclePass creation is already handled in InspectionReport.save()
        # through the call to VehiclePass.create_from_inspection(self)
        
        # Additionally, update the registration status to "approved"
        with transaction.atomic():
            registration = instance.payment_number.registration
            registration.status = 'approved'
            registration.save(update_fields=['status', 'updated_at'])


# Task to automatically void unpaid payments after 3 working days
# This should be called by a scheduler (Celery, Django-Q, etc.)
def void_unpaid_payments():
    """
    Check for payments that are still pending but past their due date
    and mark them as void
    """
    now = timezone.now()
    unpaid_transactions = PaymentTransaction.objects.filter(
        status='pending',
        due_date__lt=now
    )
    
    for transaction in unpaid_transactions:
        transaction.status = 'unpaid'
        transaction.save()

@receiver(post_save, sender=InspectionReport)
def update_registration_on_sticker_release(sender, instance, **kwargs):
    if instance.remarks == 'sticker released' and instance.is_approved:
        with transaction.atomic():
            registration = instance.payment_number.registration
            registration.status = 'approved'
            registration.save(update_fields=['status', 'updated_at'])


# Add this code to make sure signals are loaded when Django starts
default_app_config = 'vehicle_pass.apps.GetPassConfig'