from django.contrib import admin
from .models import CustomUser
from .models import Customer_info
# Register your models here.

@admin.register(Customer_info)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("Name","Mobile_No","Invoice_no","Invoice_date","Amount","Token_id")



admin.site.register(CustomUser)