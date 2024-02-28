from rest_framework import serializers
from .models import Customer_info, CustomUser
import re
class Customer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_info
        fields = "__all__"



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