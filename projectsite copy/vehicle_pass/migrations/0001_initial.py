# Generated by Django 5.1.7 on 2025-03-22 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashierProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cashier_id', models.CharField(max_length=15)),
                ('job_title', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('registrationNumber', models.BigAutoField(primary_key=True, serialize=False)),
                ('files', models.URLField(max_length=250)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('cancelled', 'Cancelled'), ('for payment', 'For Payment'), ('reviewing documents', 'Reviewing Documents'), ('for final inspection', 'For Final Inspection'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SecurityProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badgeNumber', models.CharField(max_length=10)),
                ('job_title', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('corporate_email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('cashier', 'Cashier'), ('security', 'Security')], default='user', max_length=20)),
                ('lastname', models.CharField(max_length=25)),
                ('firstname', models.CharField(max_length=50)),
                ('middle_initial', models.CharField(blank=True, max_length=25, null=True)),
                ('suffix', models.CharField(blank=True, max_length=5, null=True)),
                ('dl_number', models.CharField(blank=True, max_length=15, null=True)),
                ('college', models.CharField(blank=True, max_length=100, null=True)),
                ('program', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receipt_number', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('unpaid', 'Unpaid'), ('void', 'Void')], default='pending', max_length=10)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('cashier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.cashierprofile')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.registration')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InspectionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('inspection_date', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.CharField(choices=[('sticker_released', 'Sticker Released'), ('application_declined', 'Application Declined'), ('request_refund', 'To Request Refund')], default='sticker_released', max_length=30)),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('payment_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.paymenttransaction')),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.securityprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='securityprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.userprofile'),
        ),
        migrations.AddField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.userprofile'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('system', 'System'), ('user', 'User'), ('alert', 'Alert')], max_length=20)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cashierprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.userprofile'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcements', to='vehicle_pass.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin_id', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plateNumber', models.CharField(max_length=10, unique=True)),
                ('type', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('chassisNumber', models.CharField(max_length=17)),
                ('OR_Number', models.CharField(max_length=15)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='registration',
            name='plate_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.vehicle'),
        ),
        migrations.CreateModel(
            name='VehiclePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('passNumber', models.CharField(max_length=10)),
                ('passExpire', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('revoked', 'Revoked')], max_length=10)),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vehicle_pass.vehicle')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
