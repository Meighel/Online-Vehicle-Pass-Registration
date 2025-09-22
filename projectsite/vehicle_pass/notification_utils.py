# vehicle_pass/notification_utils.py

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from . import models
from .models import Notification, NotificationQueue, EmailTemplate, Registration, UserProfile
import logging

logger = logging.getLogger(__name__)

def create_registration_notification(registration):
    """Create notification when registration status changes"""
    user = registration.user
    
    # Status message mapping
    status_messages = {
        'application submitted': {
            'title': 'Application Submitted Successfully',
            'message': f'Your vehicle registration application #{registration.registration_number} has been submitted and is under review.',
            'email_subject': 'Vehicle Pass Application Submitted',
        },
        'initial approval': {
            'title': 'Initial Approval Received',
            'message': f'Your application #{registration.registration_number} has received initial approval from OIC.',
            'email_subject': 'Vehicle Pass Application - Initial Approval',
        },
        'final approval': {
            'title': 'Final Approval Pending',
            'message': f'Your application #{registration.registration_number} is waiting for final approval from GSO Director.',
            'email_subject': 'Vehicle Pass Application - Final Approval Pending',
        },
        'approved': {
            'title': 'Application Approved!',
            'message': f'Congratulations! Your vehicle pass application #{registration.registration_number} has been approved.',
            'email_subject': 'Vehicle Pass Application Approved',
        },
        'sticker released': {
            'title': 'Vehicle Pass Sticker Ready',
            'message': f'Your vehicle pass sticker for application #{registration.registration_number} is ready for pickup.',
            'email_subject': 'Vehicle Pass Sticker Ready for Pickup',
        },
        'rejected': {
            'title': 'Application Rejected',
            'message': f'Unfortunately, your application #{registration.registration_number} has been rejected. Please check remarks for details.',
            'email_subject': 'Vehicle Pass Application Rejected',
        }
    }
    
    status_info = status_messages.get(registration.status.lower())
    if not status_info:
        return  # Unknown status
    
    # Create in-app notification
    notification = Notification.objects.create(
        recipient=user,
        title=status_info['title'],
        message=status_info['message'],
        notification_type='application_update',
        action_url='/user/pass-status/'
    )
    
    # Create email notification in queue
    email_body = f"""
    Dear {user.firstname} {user.lastname},
    
    {status_info['message']}
    
    Registration Details:
    - Registration Number: {registration.registration_number}
    - Vehicle: {registration.vehicle.make_model} ({registration.vehicle.plate_number})
    - Status: {registration.status.title()}
    {f"- Remarks: {registration.remarks}" if registration.remarks else ""}
    
    You can check your application status at: {settings.SITE_URL}/user/pass-status/
    
    Best regards,
    Veripass Official (PalSU-GSO)
    """
    
    NotificationQueue.objects.create(
        recipient=user,
        notification_type='application_update',
        title=status_info['title'],
        message=status_info['message'],
        email_subject=status_info['email_subject'],
        email_body=email_body,
        related_object_type='registration',
        related_object_id=registration.id
    )
    
    # Try to send email immediately (since no background workers)
    try_send_email_immediately(user.corporate_email, 
                              status_info['email_subject'], 
                              email_body)

def try_send_email_immediately(recipient_email, subject, body):
    """Try to send email immediately, queue if fails"""
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False
        )
        logger.info(f"Email sent successfully to {recipient_email}")
        
        # Mark as sent in queue
        NotificationQueue.objects.filter(
            recipient__corporate_email=recipient_email,
            email_subject=subject,
            status='pending'
        ).update(
            status='sent',
            processed_at=timezone.now()
        )
        
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        # Email will remain in queue for retry

def create_announcement_notification(announcement):
    """Create notifications for announcements"""
    # Determine recipients based on announcement settings
    if announcement.send_to_all:
        recipients = UserProfile.objects.filter(role='user')
    else:
        recipients = UserProfile.objects.filter(school_role__in=announcement.target_roles)
    
    # Create in-app notifications for all recipients
    notifications = []
    for user in recipients:
        notification = Notification.objects.create(
            recipient=user,
            title=announcement.title,
            message=announcement.message,
            notification_type='system_announcement'
        )
        notifications.append(notification)
        
        # Queue email if enabled
        if announcement.send_email:
            NotificationQueue.objects.create(
                recipient=user,
                notification_type='system_announcement',
                title=announcement.title,
                message=announcement.message,
                email_subject=f"Announcement: {announcement.title}",
                email_body=f"""
                {announcement.title}
                
                {announcement.message}
                
                Posted by: {announcement.posted_by.firstname} {announcement.posted_by.lastname}
                Date: {announcement.date_posted.strftime('%B %d, %Y at %I:%M %p')}
                
                Best regards,
                PSU Vehicle Pass System
                """
            )
    
    return notifications

def process_email_queue(limit=10):
    """Process pending emails from queue (called by scheduled task)"""
    pending_emails = NotificationQueue.objects.filter(
        status='pending',
        attempts__lt=models.F('max_attempts'),
        scheduled_for__lte=timezone.now()
    ).order_by('created_at')[:limit]
    
    sent_count = 0
    failed_count = 0
    
    for email_notification in pending_emails:
        try:
            # Mark as processing
            email_notification.status = 'processing'
            email_notification.attempts += 1
            email_notification.save()
            
            # Send email
            send_mail(
                subject=email_notification.email_subject,
                message=email_notification.email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_notification.recipient.corporate_email],
                fail_silently=False
            )
            
            # Mark as sent
            email_notification.status = 'sent'
            email_notification.processed_at = timezone.now()
            email_notification.save()
            
            sent_count += 1
            logger.info(f"Email sent to {email_notification.recipient.corporate_email}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            
            # Mark as failed if max attempts reached
            if email_notification.attempts >= email_notification.max_attempts:
                email_notification.status = 'failed'
            else:
                email_notification.status = 'pending'
                # Retry later
                email_notification.scheduled_for = timezone.now() + timezone.timedelta(minutes=30)
            
            email_notification.save()
            failed_count += 1
    
    return sent_count, failed_count

def get_user_notifications(user, unread_only=False, limit=20):
    """Get notifications for a user"""
    notifications = Notification.objects.filter(recipient=user)
    
    if unread_only:
        notifications = notifications.filter(is_read=False)
    
    # Remove expired notifications
    notifications = notifications.filter(
        models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=timezone.now())
    )
    
    return notifications.order_by('-created_at')[:limit]

def mark_all_notifications_read(user):
    """Mark all notifications as read for a user"""
    return Notification.objects.filter(
        recipient=user,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )