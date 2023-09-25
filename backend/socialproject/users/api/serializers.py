from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

class UserRegisterSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
    
    def validate_email(self, value):
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address is already in use.")
        return value
    
    def validate_username(self, value):
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value
    
    def validate(self, data):
        
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password1'],  
        )
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    

class EmailSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")
        
        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")
        
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
       
        return data

    def save(self, user):
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('photo',)
        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'photo')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance