from django.contrib import admin
from .models import CustomUser
from .models import Customer_info, Draw_date
# Register your models here.

@admin.register(Customer_info)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("Name","Mobile_No","Invoice_no","Invoice_date","Amount","Token_id","dr_date")



admin.site.register(CustomUser)

admin.site.register(Draw_date)
