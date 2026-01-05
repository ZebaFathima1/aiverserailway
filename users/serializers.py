from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'phone', 'college', 
                  'password', 'password_confirm', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        from django.contrib.auth import authenticate
        
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include email and password")
        
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'phone', 'college', 'department', 'year_of_study',
                  'profile_image', 'profile_image_url', 'is_admin', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'created_at', 'updated_at']
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for admin user management"""
    profile_image_url = serializers.SerializerMethodField()
    total_payments = serializers.SerializerMethodField()
    total_registrations = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False) # Optional for updates, required for create logic can be handled
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'phone', 'college', 'department', 'year_of_study',
                  'profile_image_url', 'is_admin', 'is_active', 'created_at', 
                  'total_payments', 'total_registrations', 'password']
        read_only_fields = ['id', 'created_at']
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None
    
    def get_total_payments(self, obj):
        return obj.payment_set.count()
    
    def get_total_registrations(self, obj):
        return obj.eventregistration_set.count()
        
    def create(self, validated_data):
        password = validated_data.pop('password', 'password123') # Default password if not provided
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    """Serializer for JWT tokens"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserProfileSerializer()
