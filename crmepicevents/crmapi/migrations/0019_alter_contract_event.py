# Generated by Django 4.1.7 on 2023-06-01 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmapi', '0018_alter_contract_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_event', to='crmapi.event', unique=True, verbose_name='Event'),
        ),
    ]
