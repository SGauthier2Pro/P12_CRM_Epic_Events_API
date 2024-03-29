# Generated by Django 4.1.7 on 2023-03-22 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapi', '0013_alter_event_attendees_alter_event_event_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(blank=True, default='1900-01-01', verbose_name='Event date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.IntegerField(choices=[(0, 'In Development'), (1, 'Waiting Customer'), (2, 'Action Required'), (3, 'Terminated'), (4, 'Cancelled')], default=0, verbose_name='Event status'),
        ),
    ]
