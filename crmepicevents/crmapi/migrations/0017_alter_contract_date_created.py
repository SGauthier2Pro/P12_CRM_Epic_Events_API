# Generated by Django 4.1.7 on 2023-04-11 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapi', '0016_alter_contract_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
        ),
    ]