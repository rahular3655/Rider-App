# Generated by Django 5.0.1 on 2024-02-03 07:39

import django.db.models.deletion
import django_lifecycle.mixins
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(blank=True, choices=[('bike', 'Bike'), ('scooter', 'Scooter'), ('car', 'Car')], max_length=100, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=100, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='Requested', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rides_requested', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('started', 'Started'), ('ended', 'Ended'), ('cancelled', 'Cancelled')], default='Started', max_length=100, null=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_driver', to='ride.driver')),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='ride.ride')),
            ],
        ),
    ]
