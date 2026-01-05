from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    payment_screenshot_url = serializers.SerializerMethodField()
    processed_by_email = serializers.EmailField(source='processed_by.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'user_name', 'user_phone', 'event', 
                  'event_title', 'amount', 'transaction_id', 'payment_screenshot',
                  'payment_screenshot_url', 'status', 'notes', 'submitted_at', 
                  'processed_at', 'processed_by', 'processed_by_email']
        read_only_fields = ['id', 'submitted_at', 'processed_at', 'processed_by']
    
    def get_payment_screenshot_url(self, obj):
        request = self.context.get('request')
        if obj.payment_screenshot and request:
            return request.build_absolute_uri(obj.payment_screenshot.url)
        return None
