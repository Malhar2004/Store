from django.db import models
import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,MinLengthValidator, MaxLengthValidator
# Create your models here.
from django.core.exceptions import ValidationError


from rest_framework.exceptions import ValidationError

def validate_positive(value):
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
                regex='^[a-zA-Z\s]*$',
                message='Name must contain only letters.',
                code='invalid_name'
            )
        ])
    Mobile_No = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$'),MinLengthValidator(10),
            MaxLengthValidator(10)])
    Invoice_no = models.CharField(max_length=70, unique=True, validators=[validate_positive])
    Invoice_date = models.DateField()
    time = models.TimeField(auto_now_add = True)
    Amount = models.PositiveIntegerField()
    Token_id = models.CharField(unique=True, editable=False)
    dr_date = models.DateField(default=None)

############ Function #############################
    def save(self, *args, **kwargs):
        # Generate a unique 6-digit integer ID
        if not self.Token_id:
            id_length = 6  # Initial length of the unique ID
            while True:
                min_id = 10 ** (id_length - 1)
                max_id = (10 ** id_length) - 1
                unique_id = random.randint(min_id, max_id)
                if not Customer_info.objects.filter(Token_id=unique_id).exists():
                    self.Token_id = unique_id
                    break
            # Check if all possible IDs of this length are exhausted
            if Customer_info.objects.count() == (max_id - min_id + 1):
                id_length += 1  # Increase the length for the next iteration

        super(Customer_info, self).save(*args, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username


class Draw_date(models.Model):
    dr_date = models.DateField(default=None)


    def __str__(self):
        return str(self.dr_date)



class Deleted_records(models.Model):
    Name = models.CharField(max_length=70,  validators=[RegexValidator(
                regex='^[a-zA-Z\s]*$',
                message='Name must contain only letters.',
                code='invalid_name'
            )
        ])
    Mobile_No = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$'),MinLengthValidator(10),
            MaxLengthValidator(10)])
    Invoice_no = models.CharField(max_length=70, unique=True, validators=[validate_positive])
    Invoice_date = models.DateField()
    Amount = models.PositiveIntegerField()
    Token_id = models.CharField(max_length=20, unique=True)
    dr_date = models.DateField(default=None)
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    IP_Address = models.GenericIPAddressField()