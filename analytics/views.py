from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from events.models import Event
from payments.models import Payment
from .models import Activity
from users.views import IsAdminUser

User = get_user_model()


from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request):
    """Dashboard analytics endpoint"""
    user_email = request.user.email if not request.user.is_anonymous else "Anonymous"
    is_admin = request.user.is_admin if not request.user.is_anonymous else False
    print(f"Analytics dashboard accessed by: {user_email} (Admin: {is_admin})")
    
    # Get date range for chart data (last 30 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Basic stats
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_payments = Payment.objects.count()
    pending_payments = Payment.objects.filter(status='pending').count()
    approved_payments = Payment.objects.filter(status='approved').count()
    
    # Revenue stats
    total_revenue = Payment.objects.filter(status='approved').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    pending_revenue = Payment.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Recent activities (last 10)
    recent_activities = Activity.objects.select_related('user').order_by('-timestamp')[:10]
    activities_data = [
        {
            'id': activity.id,
            'user': activity.user.full_name or activity.user.email,
            'action': activity.action,
            'type': activity.activity_type,
            'time': activity.timestamp.isoformat(),
        }
        for activity in recent_activities
    ]
    
    # Chart data - registrations over time
    registrations_by_day = []
    for i in range(30):
        day = start_date + timedelta(days=i)
        next_day = day + timedelta(days=1)
        count = User.objects.filter(
            created_at__gte=day,
            created_at__lt=next_day
        ).count()
        registrations_by_day.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Payment status distribution
    payment_status_distribution = [
        {'status': 'Pending', 'count': pending_payments},
        {'status': 'Approved', 'count': approved_payments},
        {'status': 'Rejected', 'count': Payment.objects.filter(status='rejected').count()},
    ]
    
    # Event status distribution
    event_status_distribution = [
        {'status': 'Upcoming', 'count': Event.objects.filter(status='upcoming').count()},
        {'status': 'Ongoing', 'count': Event.objects.filter(status='ongoing').count()},
        {'status': 'Completed', 'count': Event.objects.filter(status='completed').count()},
    ]
    
    return Response({
        'stats': {
            'total_users': total_users,
            'total_events': total_events,
            'active_events': Event.objects.filter(status='upcoming').count() + Event.objects.filter(status='ongoing').count(),
            'total_registrations': total_payments,
            'total_payments': total_payments,
            'pending_payments': pending_payments,
            'approved_payments': approved_payments,
            'total_revenue': float(total_revenue),
            'pending_revenue': float(pending_revenue),
        },
        'activities': activities_data,
        'chart_data': {
            'registrations_by_day': registrations_by_day,
            'payment_status_distribution': payment_status_distribution,
            'event_status_distribution': event_status_distribution,
        }
    })
