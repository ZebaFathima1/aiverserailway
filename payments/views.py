from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Payment
from .serializers import PaymentSerializer
from users.views import IsAdminUser
from analytics.models import Activity


from rest_framework.permissions import IsAuthenticated, AllowAny

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for payment management"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_permissions(self):
        if self.action in ['approve', 'reject', 'list', 'retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Payment.objects.select_related('user', 'event', 'processed_by')
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by user (for non-admin users)
        if hasattr(self.request.user, 'is_admin'):
            if not self.request.user.is_admin:
                queryset = queryset.filter(user=self.request.user)
        elif self.request.user.is_anonymous:
            # Allow listing for admin dashboard via API if we are using AllowAny for list
            # But normally we'd restrict.
            pass
        
        return queryset.order_by('-submitted_at')
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Resolve User
        user = None
        if request.user.is_authenticated:
            user = request.user
        else:
            email = data.get('email')
            if not email:
                return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found. Please register first.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Resolve Event
        from events.models import Event
        event = Event.objects.filter(slug='ai-verse-4').first()
        if not event:
            event = Event.objects.filter(status='upcoming').first()
            
        # Prepare data for serializer
        data['user'] = user.id
        if event:
            data['event'] = event.id
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, user=None):
        if not user:
            user = self.request.user if self.request.user.is_authenticated else None
            
        serializer.save(user=user)
        
        # Create activity log
        if user:
            Activity.objects.create(
                user=user,
                action='submitted a payment',
                activity_type='payment'
            )
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def approve(self, request, pk=None):
        """Approve a payment"""
        payment = self.get_object()
        payment.status = 'approved'
        payment.processed_at = timezone.now()
        payment.processed_by = request.user if not request.user.is_anonymous else None
        payment.save()
        
        # Create activity log
        Activity.objects.create(
            user=payment.user,
            action=f'payment approved for {payment.event.title if payment.event else "registration"}',
            activity_type='payment'
        )
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def reject(self, request, pk=None):
        """Reject a payment"""
        payment = self.get_object()
        payment.status = 'rejected'
        payment.processed_at = timezone.now()
        payment.processed_by = request.user if not request.user.is_anonymous else None
        payment.notes = request.data.get('notes', payment.notes)
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
