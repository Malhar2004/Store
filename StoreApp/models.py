from django.db import models
import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,MinLengthValidator, MaxLengthValidator
# Create your models here.
from django.core.exceptions import ValidationError


def validate_positive(value):
    if value < 0:
        raise ValidationError('Value cannot be negative.')

class Customer_info(models.Model):
    Name = models.CharField(max_length=70,  validators=[RegexValidator(
                regex='^[a-zA-Z\s]*$',
                message='Name must contain only letters.',
                code='invalid_name'
            )
        ])
    Mobile_No = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$'),MinLengthValidator(10),
            MaxLengthValidator(10)])
    Invoice_no = models.BigIntegerField(unique=True, validators=[validate_positive])
    Invoice_date = models.DateField()
    Amount = models.PositiveIntegerField()
    Token_id = models.IntegerField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate a unique 6-digit integer ID
        while True:
            unique_id = random.randint(100000, 999999)
            if not Customer_info.objects.filter(Token_id=unique_id).exists():
                self.Token_id = unique_id
                break

        super(Customer_info, self).save(*args, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username


