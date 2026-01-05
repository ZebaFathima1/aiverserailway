from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Activity(models.Model):
    """Activity tracking model"""
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('registration', 'Registration'),
        ('payment', 'Payment'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, default='other')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.user.email} - {self.action}"
