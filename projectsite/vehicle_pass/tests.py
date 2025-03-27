from django.test import TestCase
from django.utils import timezone
from .models import (
    UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, VehiclePass, PaymentTransaction,
    InspectionReport, Notification, Announcement
)


class ModelTestCase(TestCase):

    def setUp(self):
        # Create a UserProfile
        self.user = UserProfile.objects.create(
            corporate_email="test@example.com",
            password="securepass",
            firstname="John",
            lastname="Doe",
            address="123 Street"
        )

        # Create different profiles linked to UserProfile
        self.security = SecurityProfile.objects.create(
            user=self.user, badgeNumber="SEC123", job_title="Guard"
        )

        self.cashier = CashierProfile.objects.create(
            user=self.user, cashier_id="CASH123", job_title="Cashier"
        )

        self.admin = AdminProfile.objects.create(
            user=self.user, admin_id="ADM123"
        )

        # Create a Vehicle
        self.vehicle = Vehicle.objects.create(
            owner=self.user, plateNumber="ABC123", type="Sedan",
            model="Toyota", color="Blue", chassisNumber="CHS12345",
            OR_Number="OR98765"
        )

        # Create a Registration
        self.registration = Registration.objects.create(
            user=self.user, plate_number=self.vehicle, files="http://example.com/doc.pdf"
        )

        # Create a PaymentTransaction
        self.payment = PaymentTransaction.objects.create(
            registration=self.registration, receipt_number="REC123",
            cashier=self.cashier, status="paid"
        )

        # Create an InspectionReport
        self.inspection = InspectionReport.objects.create(
            payment_number=self.payment, security=self.security,
            remarks="sticker_released", additional_notes="All good", is_approved=True
        )

        # Create a VehiclePass
        self.vehicle_pass = VehiclePass.objects.create(
            vehicle=self.vehicle, passNumber="VP123", passExpire=timezone.now().date(), status="active"
        )

        # Create a Notification
        self.notification = Notification.objects.create(
            type="alert", message="Test notification", recipient=self.user
        )

        # Create an Announcement
        self.announcement = Announcement.objects.create(
            title="Test Announcement", message="This is a test announcement", posted_by=self.user
        )

    def test_user_creation(self):
        """Test UserProfile creation"""
        self.assertEqual(self.user.firstname, "John")
        self.assertEqual(self.user.lastname, "Doe")

    def test_security_profile_creation(self):
        """Test SecurityProfile creation"""
        self.assertEqual(self.security.badgeNumber, "SEC123")
        self.assertEqual(self.security.job_title, "Guard")

    def test_cashier_profile_creation(self):
        """Test CashierProfile creation"""
        self.assertEqual(self.cashier.cashier_id, "CASH123")

    def test_admin_profile_creation(self):
        """Test AdminProfile creation"""
        self.assertEqual(self.admin.admin_id, "ADM123")

    def test_vehicle_creation(self):
        """Test Vehicle creation"""
        self.assertEqual(self.vehicle.plateNumber, "ABC123")

    def test_registration_creation(self):
        """Test Registration creation"""
        self.assertEqual(self.registration.files, "http://example.com/doc.pdf")

    def test_payment_transaction_creation(self):
        """Test PaymentTransaction creation"""
        self.assertEqual(self.payment.receipt_number, "REC123")
        self.assertEqual(self.payment.status, "paid")

    def test_inspection_report_creation(self):
        """Test InspectionReport creation"""
        self.assertTrue(self.inspection.is_approved)

    def test_vehicle_pass_creation(self):
        """Test VehiclePass creation"""
        self.assertEqual(self.vehicle_pass.passNumber, "VP123")

    def test_notification_creation(self):
        """Test Notification creation"""
        self.assertEqual(self.notification.message, "Test notification")

    def test_announcement_creation(self):
        """Test Announcement creation"""
        self.assertEqual(self.announcement.title, "Test Announcement")


if __name__ == "__main__":
    TestCase.main()
