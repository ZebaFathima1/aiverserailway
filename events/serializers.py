from rest_framework import serializers
from .models import Event, EventImage, EventRegistration


class EventImageSerializer(serializers.ModelSerializer):
    """Serializer for event images"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = EventImage
        fields = ['id', 'image', 'image_url', 'caption', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class EventSerializer(serializers.ModelSerializer):
    """Serializer for events"""
    images = EventImageSerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    total_registrations = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'description', 'short_description', 
                  'date', 'end_date', 'venue', 'registration_fee', 'max_participants',
                  'status', 'highlights', 'gallery_dir', 'cover_image_name', 'cover_image_url',
                  'featured_image', 'featured_image_url', 'is_featured',
                  'images', 'total_registrations', 'is_full', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_featured_image_url(self, obj):
        request = self.context.get('request')
        if obj.featured_image and request:
            return request.build_absolute_uri(obj.featured_image.url)
        return None

    def get_cover_image_url(self, obj):
        if obj.gallery_dir:
            return f"/gallery/{obj.gallery_dir}/{obj.cover_image_name}"
        return None


class EventRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for event registrations"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'user_email', 'user_name', 'event', 'event_title',
                  'registered_at', 'is_active']
        read_only_fields = ['id', 'registered_at']
