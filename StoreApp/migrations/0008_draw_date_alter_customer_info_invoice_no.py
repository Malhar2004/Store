# Generated by Django 5.0.2 on 2024-03-04 04:34

import StoreApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreApp', '0007_alter_customer_info_invoice_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dr_date', models.DateField(default=None)),
            ],
        ),
        migrations.AlterField(
            model_name='customer_info',
            name='Invoice_no',
            field=models.CharField(max_length=70, unique=True, validators=[StoreApp.models.validate_positive]),
        ),
    ]
