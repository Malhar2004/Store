# Generated by Django 5.0.1 on 2024-03-08 14:01

import StoreApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreApp', '0016_alter_customer_info_invoice_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_info',
            name='Invoice_no',
            field=models.CharField(max_length=70, validators=[StoreApp.models.validate_positive]),
        ),
    ]