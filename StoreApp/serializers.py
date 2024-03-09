from rest_framework import serializers
from .models import Customer_info, CustomUser, Draw_date
import re
from django.core.exceptions import ValidationError
from .utils import get_client_ip
import random
from django.utils import timezone
import pytz


class Customer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_info
        fields = "__all__"

    def validate(self, data):
        invoice_date = data.get('Invoice_date')
        if invoice_date:
            draw_dates = Draw_date.objects.all()
            if draw_dates.exists():
                draw_date = draw_dates.latest('dr_date').dr_date
                if invoice_date > draw_date:
                    raise ValidationError("kindly change the draw date.")
        return data
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.is_deleted:
            ret['is_deleted'] = True
        return ret

    def create(self, validated_data):
        id_length = 6  # Initial length of the unique ID
        while True:
            min_id = 10 ** (id_length - 1)
            max_id = (10 ** id_length) - 1
            unique_id = random.randint(min_id, max_id)
            if not Customer_info.objects.filter(Token_id=unique_id, is_deleted=False).exists():
                validated_data['Token_id'] = unique_id
                break
        # Check if all possible IDs of this length are exhausted
        if Customer_info.objects.count() == (max_id - min_id + 1):
            id_length += 1  # Increase the length for the next iteration

        # Set the time field to the current time
        indian_tz = pytz.timezone('Asia/Kolkata')
        validated_data['time'] = timezone.now().astimezone(indian_tz).strftime('%H:%M')


        return super().create(validated_data)



    def update(self, instance, validated_data): 
        instance.Name = validated_data.get('Name', instance.Name)
        instance.Mobile_No = validated_data.get('Mobile_No', instance.Mobile_No)
        instance.Invoice_no = validated_data.get('Invoice_no', instance.Invoice_no)
        instance.Invoice_date = validated_data.get('Invoice_date', instance.Invoice_date)
        instance.Amount = validated_data.get('Amount', instance.Amount)
        instance.dr_date = validated_data.get('dr_date', instance.dr_date)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        # Update deleted_by_ip only if the instance is being soft-deleted
        if instance.is_deleted:
            instance.deleted_by_ip = validated_data.get('deleted_by_ip', instance.deleted_by_ip)
        
        instance.save()
        return instance
    




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user






class Draw_date_serializer(serializers.ModelSerializer):
    class Meta:
        model = Draw_date
        fields = "__all__"

    # def validate_dr_date(self, value):
    #     latest_invoice_date = Customer_info.objects.latest('Invoice_date').Invoice_date
    #     if value < latest_invoice_date:
    #         raise serializers.ValidationError("Please change the draw date")
    #     return value
    