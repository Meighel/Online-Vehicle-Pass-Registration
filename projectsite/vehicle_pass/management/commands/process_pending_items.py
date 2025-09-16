# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# from ...models import Registration, PaymentTransaction


# class Command(BaseCommand):
#     help = 'Processes time-dependent status updates for registrations and payments'

#     def handle(self, *args, **options):
#         self.stdout.write('Processing pending registrations and payments...')
        
#         # 1. Auto-change pending registrations to "reviewing documents" after 5 working days
#         five_days_ago = timezone.now() - timedelta(days=5)
#         pending_registrations = Registration.objects.filter(
#             status='pending',
#             created_at__lt=five_days_ago
#         )
        
#         registration_count = pending_registrations.count()
#         if registration_count > 0:
#             pending_registrations.update(status='reviewing documents')
#             self.stdout.write(
#                 self.style.SUCCESS(f'Updated {registration_count} pending registrations to "reviewing documents"')
#             )
        
#         # 3. Auto-void payments that are pending for more than 3 working days
#         three_days_ago = timezone.now() - timedelta(days=3)
#         pending_payments = PaymentTransaction.objects.filter(
#             status='pending',
#             created_at__lt=three_days_ago
#         )
        
#         payment_count = pending_payments.count()
#         if payment_count > 0:
#             for payment in pending_payments:
#                 payment.status = 'cancelled'
#                 payment.save()  # Using save() to trigger any signals attached to payment
            
#             self.stdout.write(
#                 self.style.SUCCESS(f'Cancelled {payment_count} pending payments older than 3 days')
#             )
        
#         self.stdout.write(self.style.SUCCESS('Completed processing registrations and payments'))