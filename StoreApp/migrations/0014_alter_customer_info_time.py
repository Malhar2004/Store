# Generated by Django 5.0.1 on 2024-03-08 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreApp', '0013_delete_deleted_records_customer_info_deleted_by_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_info',
            name='time',
            field=models.CharField(editable=False, max_length=5),
        ),
    ]