from django.contrib.auth.models import User
from rest_framework import serializers

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