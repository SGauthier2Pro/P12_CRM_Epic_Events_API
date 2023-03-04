# Generated by Django 4.1.7 on 2023-03-01 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapi', '0002_remove_contract_sales_contact_contract_event_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='client',
        ),
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.IntegerField(choices=[(0, 'In Development'), (1, 'Waiting Customer'), (2, 'Action Required'), (3, 'Terminated'), (4, 'Cancelled')], default=0, verbose_name='Event status'),
        ),
    ]
