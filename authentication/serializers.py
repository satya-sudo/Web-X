from re import U
from rest_framework import serializers
from .models import User
from django.contrib import auth


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','username','password']

    def validate(self, attrs):
        phone = attrs.get('phone','')
        username = attrs.get('username','')
        password = attrs.get('password','')

        # TODO
        # add regix validations for phone and password

        if phone and username and password:
            return attrs
        else:
            raise serializers.ValidationError('phone, username, password is required')

    def create(self, validated_data):
        phone = validated_data.get('phone','')
        username = validated_data.get('username','')
        password = validated_data.get('password','')
        user = User.objects.create(phone=phone,username=username,password=password)
        return user


class LoginSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(max_length=50, write_only=True)
    username = serializers.CharField(max_length=50, read_only=True)
    tokens = serializers.CharField(max_length=68, required=False, read_only=True)

    class Meta:
        model = User
        fields = ['phone','password','username','tokens']
        extra_kwargs = {
            'password': {'write_only': True},
            'tokens': {'read_only': True}
        }

    def validate(self, attrs):
        phone = attrs.get('phone','')
        password = attrs.get('password','')

        user = auth.authenticate(phone=phone, password=password)

        if not user:
            raise serializers.ValidationError('Invalid phone or password')
        
        return {
            'phone': user.phone,
            'username': user.username,
            'tokens': user.tokens()
    
        }
