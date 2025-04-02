from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from vehicle_pass.models import (
    UserProfile, SecurityProfile, CashierProfile, AdminProfile,
    Vehicle, Registration, VehiclePass, PaymentTransaction, 
    InspectionReport, Notification, Announcement
)

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            corporate_email="testuser@example.com",
            password="securepassword",
            lastname="Doe",
            firstname="John",
            address="123 Main St",
            role="user"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.firstname, "John")
        self.assertEqual(self.user.lastname, "Doe")
        self.assertEqual(self.user.role, "user")


class VehicleTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            corporate_email="vehicleowner@example.com",
            password="securepassword",
            lastname="Smith",
            firstname="Alice",
            address="456 Elm St",
            role="user"
        )
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            plateNumber="XYZ1234",
            type="Sedan",
            model="Toyota",
            color="Blue",
            chassisNumber="123456789ABCDEFG",
            OR_Number="OR1234567"
        )
    
    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.plateNumber, "XYZ1234")
        self.assertEqual(self.vehicle.owner, self.user)
    
    def test_vehicle_limit(self):
        # Create first vehicle - should succeed
        Vehicle.objects.create(
            owner=self.user,
            plateNumber="ABC5678",
            type="SUV",
            model="Honda",
            color="Red",
            chassisNumber="987654321HGFEDCBA",
            OR_Number="OR7654321"
        )

        # Create second vehicle - should succeed
        Vehicle.objects.create(
            owner=self.user,
            plateNumber="DEF9101",
            type="Truck",
            model="Ford",
            color="Black",
            chassisNumber="11223344556677889",
            OR_Number="OR9988776"
        )

        # Try to create third vehicle - should raise ValidationError
        with self.assertRaises(ValidationError):
            vehicle = Vehicle(
                owner=self.user,
                plateNumber="GHI1122",
                type="Coupe",
                model="BMW",
                color="White",
                chassisNumber="445566778899AABB",
                OR_Number="OR1122334"
            )
            vehicle.full_clean()  # ✅ Triggers validation
            vehicle.save()  # ✅ This should raise ValidationError



class RegistrationTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            corporate_email="reguser@example.com",
            password="securepassword",
            lastname="Brown",
            firstname="Charlie",
            address="789 Pine St",
            role="user"
        )
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            plateNumber="DEF4567",
            type="Sedan",
            model="Tesla",
            color="White",
            chassisNumber="A1B2C3D4E5F6G7H8I",
            OR_Number="OR4567890"
        )
        self.registration = Registration.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            files="https://example.com/docs",
            status="pending"
        )

    def test_registration_creation(self):
        self.assertEqual(self.registration.status, "pending")
        self.assertEqual(self.registration.user, self.user)
        self.assertEqual(self.registration.vehicle, self.vehicle)


class PaymentTransactionTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            corporate_email="payuser@example.com",
            password="securepassword",
            lastname="Wilson",
            firstname="Ethan",
            address="Pay St",
            role="user"
        )
        self.cashier = CashierProfile.objects.create(
            user=self.user,
            cashier_id="CASH123",
            job_title="Head Cashier"
        )
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            plateNumber="JKL7890",
            type="SUV",
            model="Nissan",
            color="Gray",
            chassisNumber="B2C3D4E5F6G7H8I9J",
            OR_Number="OR5678901"
        )
        self.registration = Registration.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            files="https://example.com/payment_docs",
            status="for payment"
        )
        self.payment = PaymentTransaction.objects.create(
            registration=self.registration,
            receipt_number="REC12345",
            cashier=self.cashier,
            status="paid"
        )

    def test_payment_transaction_creation(self):
        self.assertEqual(self.payment.status, "paid")
        self.assertEqual(self.payment.receipt_number, "REC12345")
        self.assertEqual(self.payment.cashier, self.cashier)


class InspectionReportTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            corporate_email="inspectuser@example.com",
            password="securepassword",
            lastname="Thomas",
            firstname="Daniel",
            address="Inspect St",
            role="user"
        )
        self.cashier = CashierProfile.objects.create(
            user=self.user,
            cashier_id="CASH123",
            job_title="Head Cashier"
        )
        self.security = SecurityProfile.objects.create(
            user=self.user,
            badgeNumber="SEC999",
            job_title="Security Officer"
        )
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            plateNumber="MNO2345",
            type="Truck",
            model="Chevrolet",
            color="Green",
            chassisNumber="D4E5F6G7H8I9J0K1L",
            OR_Number="OR6789012"
        )
        self.registration = Registration.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            files="https://example.com/inspection_docs",
            status="for final inspection"
        )
        self.payment = PaymentTransaction.objects.create(
            registration=self.registration,
            receipt_number="REC67890",
            cashier=self.cashier, 
            status="paid"
        )
        self.inspection = InspectionReport.objects.create(
            payment_number=self.payment,
            security=self.security,
            remarks="sticker_released",
            additional_notes="Inspection passed successfully.",
            is_approved=True
        )

    def test_inspection_report_creation(self):
        self.assertTrue(self.inspection.is_approved)
        self.assertEqual(self.inspection.remarks, "sticker_released")
        self.assertEqual(self.inspection.additional_notes, "Inspection passed successfully.")


class NotificationTestCase(TestCase):
    def setUp(self):
        self.admin = UserProfile.objects.create(
            corporate_email="admin@example.com",
            password="adminpassword",
            lastname="Admin",
            firstname="Super",
            address="Office St",
            role="admin"
        )
        self.notification = Notification.objects.create(
            type="system",
            message="System maintenance scheduled.",
            posted_by=self.admin,
            is_read=False
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.type, "system")
        self.assertEqual(self.notification.message, "System maintenance scheduled.")
        self.assertEqual(self.notification.posted_by, self.admin)
        self.assertFalse(self.notification.is_read)


class AnnouncementTestCase(TestCase):
    def setUp(self):
        self.admin = UserProfile.objects.create(
            corporate_email="announcement_admin@example.com",
            password="adminpassword",
            lastname="News",
            firstname="Broadcaster",
            address="News St",
            role="admin"
        )
        self.announcement = Announcement.objects.create(
            title="New Parking Rules",
            message="Please follow the new parking regulations effective next month.",
            posted_by=self.admin
        )

    def test_announcement_creation(self):
        self.assertEqual(self.announcement.title, "New Parking Rules")
        self.assertEqual(self.announcement.message, "Please follow the new parking regulations effective next month.")
        self.assertEqual(self.announcement.posted_by, self.admin)
