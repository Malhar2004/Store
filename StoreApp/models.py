from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
# Create your models here.




from rest_framework.exceptions import ValidationError

def validate_positive(value):
    if hasattr(value, 'is_deleted') and not value.is_deleted:
        try:
            int_value = int(value)
            if int_value < 0:
                raise ValidationError('Value must be positive.')
        except ValueError:
            if not isinstance(value, (int, float)):
                raise ValidationError('Invalid value. Must be a number.')
            else:
                raise ValidationError('Value must be positive.')



class Customer_info(models.Model):
    Name = models.CharField(max_length=70,  validators=[RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Name must contain only letters.',
                code='invalid_name'
            )
        ])
    Mobile_No = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$'),MinLengthValidator(10),
            MaxLengthValidator(10)])
    Invoice_no = models.CharField(max_length=70, unique=True, validators=[validate_positive])
    Invoice_date = models.DateField()
    time = models.CharField(max_length=5, editable=False)  # HH:MM format
    Amount = models.PositiveIntegerField()
    Token_id = models.CharField(unique=True, editable=False)
    dr_date = models.DateField(default=None)
    is_deleted = models.BooleanField(default=False)  # New field for soft delete
    deleted_by_ip = models.CharField(max_length=15, blank=True, null=True)  # Field to store the IP address of the user who soft-deleted the record

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username


class Draw_date(models.Model):
    dr_date = models.DateField(default=None)


    def __str__(self):
        return str(self.dr_date)


