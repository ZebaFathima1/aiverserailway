from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventRegistration
from payments.models import Payment

@receiver(post_save, sender=EventRegistration)
def create_payment_for_registration(sender, instance, created, **kwargs):
    if created:
        event = instance.event
        # Only create payment if there is a fee
        if event.registration_fee > 0:
            # Check if payment already exists (avoid duplicates)
            if not Payment.objects.filter(user=instance.user, event=event).exists():
                Payment.objects.create(
                    user=instance.user,
                    event=event,
                    amount=event.registration_fee,
                    status='pending',
                    notes=f"Auto-created upon registration for {event.title}"
                )
        
        # Log activity
        from analytics.models import Activity
        Activity.objects.create(
            user=instance.user,
            action=f"Registered for {event.title}",
            activity_type='registration'
        )
