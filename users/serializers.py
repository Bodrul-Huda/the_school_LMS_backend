from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializers(serializers.ModelSerializer):
  password = serializers.CharField(write_only = True, required = False)
  class Meta:
    model = User
    fields = ['id', 'username', 'mobile_no', 'role', 'email', 'password']
 
  
  def create(self, validated_data):
        if 'password' not in validated_data:
            raise serializers.ValidationError({'password': 'This field is required.'})
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
  
  def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['role'] = user.role 

        return token