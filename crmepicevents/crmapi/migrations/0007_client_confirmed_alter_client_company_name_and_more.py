# Generated by Django 4.1.7 on 2023-03-08 10:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crmapi', '0006_alter_event_event_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Confirmed client ?'),
        ),
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.CharField(max_length=250, verbose_name='Compagny name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date last update'),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(blank=True, max_length=25, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(max_length=25, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex='(0|\\+33|0033)[1-9][0-9]{8}')], verbose_name='Mobile'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex='(0|\\+33|0033)[1-9][0-9]{8}')], verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_clients', to=settings.AUTH_USER_MODEL, verbose_name='Sales contact'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='amount',
            field=models.FloatField(default='0.0', verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='crmapi.client', verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date last update'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_event', to='crmapi.event', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date of payment'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Signed ?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(blank=True, null=True, verbose_name='Attendees'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date last update'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Event date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.IntegerField(choices=[(0, 'In Development'), (1, 'Waiting Customer'), (2, 'Action Required'), (3, 'Terminated'), (4, 'Cancelled')], default=0, verbose_name='Event status'),
        ),
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_event', to=settings.AUTH_USER_MODEL, verbose_name='Support contact'),
        ),
    ]
