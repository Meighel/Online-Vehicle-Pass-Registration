from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser, UserProfile, Vehicle

class CustomUserTest(TestCase):
    def setUp(self):
        self.corporate_email = "test@example.com"
        self.password = "password123"
        self.user = CustomUser.objects.create_user(
            corporate_email=self.corporate_email,
            password=self.password,
            firstname="John",
            lastname="Doe",
            address="123 Test St"
        )

    def test_create_user(self):
        self.assertEqual(self.user.corporate_email, self.corporate_email)
        self.assertTrue(self.user.check_password(self.password))

    def test_create_user_missing_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(corporate_email=None, password="password123")

    def test_create_user_missing_password(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(corporate_email="test@example.com", password=None)

class UserProfileTest(TestCase):
    def setUp(self):
        self.corporate_email = "test@example.com"
        self.password = "password123"
        self.user = CustomUser.objects.create_user(
            corporate_email=self.corporate_email,
            password=self.password,
            firstname="John",
            lastname="Doe",
            address="123 Test St"
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.firstname, "John")
        self.assertEqual(self.profile.lastname, "Doe")

class VehicleTest(TestCase):
    def setUp(self):
        self.corporate_email = "test@example.com"
        self.password = "password123"
        self.user = CustomUser.objects.create_user(
            corporate_email=self.corporate_email,
            password=self.password,
            firstname="John",
            lastname="Doe",
            address="123 Test St"
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_vehicle_registration(self):
        vehicle = Vehicle.objects.create(
            owner=self.profile,
            plateNumber="ABC123",
            type="Sedan",
            model="2022",
            color="Black",
            chassisNumber="CHS123456",
            OR_Number="OR123456"
        )
        self.assertEqual(vehicle.owner, self.profile)
        self.assertEqual(vehicle.plateNumber, "ABC123")

    def test_vehicle_registration_limit(self):
        Vehicle.objects.create(
            owner=self.profile,
            plateNumber="ABC123",
            type="Sedan",
            model="2022",
            color="Black",
            chassisNumber="CHS123456",
            OR_Number="OR123456"
        )
        Vehicle.objects.create(
            owner=self.profile,
            plateNumber="DEF456",
            type="SUV",
            model="2023",
            color="White",
            chassisNumber="CHS789012",
            OR_Number="OR789012"
        )
        with self.assertRaises(ValidationError):
            Vehicle.objects.create(
                owner=self.profile,
                plateNumber="XYZ789",
                type="Truck",
                model="2024",
                color="Red",
                chassisNumber="CHS345678",
                OR_Number="OR345678"
            )