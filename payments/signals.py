from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from events.models import EventRegistration
from analytics.models import Activity

@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    # 1. Log Activity on Creation
    if created:
        Activity.objects.create(
            user=instance.user,
            action=f"Initiated payment of {instance.amount} for {instance.event.title if instance.event else 'Event'}",
            activity_type='payment'
        )
    
    # 2. Handle Status Changes (Approval)
    if instance.status == 'approved' and instance.event:
        # Activate the registration
        EventRegistration.objects.filter(
            user=instance.user, 
            event=instance.event
        ).update(is_active=True)
        
        # Log Approval Activity
        # Check if we haven't logged this recently to avoid duplicates if saved multiple times
        # For simplicity, we just log it.
        Activity.objects.create(
            user=instance.user,
            action=f"Payment approved for {instance.event.title}",
            activity_type='payment'
        )
