from django.test import TestCase
from django.contrib.auth import get_user_model
from vehicle_pass.models import UserProfile, CashierProfile, SecurityProfile, AdminProfile


class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user(self):
        user = self.user_model.objects.create_user(            
            corporate_email='testuser@example.com',
            password='password123',
            firstname='Test',
            lastname='User',
            role='user',
            middle_initial='A',
            suffix='Jr.',
            dl_number='123456789',
            college='Test College',
            program='CS',
            department='IT',
            address='123 Test Street'
        )

        self.assertIsInstance(user, self.user_model)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Fetch the UserProfile correctly
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.firstname, 'Test')
        self.assertEqual(profile.lastname, 'User')

    def test_create_superuser(self):
        superuser = self.user_model.objects.create_superuser(
            corporate_email='admin@example.com',
            password='admin123'
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_cashier_profile(self):
        user = self.user_model.objects.create_user(
            corporate_email='cashier@example.com',
            password='cashier123',
            role='cashier',
            firstname='Cashier',
            lastname='User',
            cashier_id='C001',
            job_title='Cashier'
        )

        # Fetch CashierProfile correctly
        cashier_profile = CashierProfile.objects.get(user__user=user)
        self.assertEqual(cashier_profile.cashier_id, 'C001')
        self.assertEqual(cashier_profile.job_title, 'Cashier')

    def test_create_security_profile(self):
        user = self.user_model.objects.create_user(
            corporate_email='security@example.com',
            password='security123',
            role='security',
            firstname='Security',
            lastname='Guard',
            badgeNumber='B123',
            job_title='Security Guard'
        )

        # Fetch SecurityProfile correctly
        security_profile = SecurityProfile.objects.get(user__user=user)
        self.assertEqual(security_profile.badgeNumber, 'B123')
        self.assertEqual(security_profile.job_title, 'Security Guard')

    def test_create_admin_profile(self):
        user = self.user_model.objects.create_user(
            corporate_email='adminuser@example.com',
            password='adminuser123',
            role='admin',
            firstname='Admin',
            lastname='User',
            admin_id='A001'
        )

        # Fetch AdminProfile correctly
        admin_profile = AdminProfile.objects.get(user__user=user)
        self.assertEqual(admin_profile.admin_id, 'A001')
