from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    """Event model"""
    EVENT_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=255)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_participants = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='upcoming')
    highlights = models.TextField(blank=True, default='[]', help_text="JSON string of highlights")
    gallery_dir = models.CharField(max_length=100, blank=True, help_text="Directory name in public/gallery/")
    cover_image_name = models.CharField(max_length=100, default='cover.jpg', help_text="Filename of the cover image in the gallery directory")
    featured_image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return self.title
    
    @property
    def total_registrations(self):
        return self.eventregistration_set.filter(is_active=True).count()
    
    @property
    def is_full(self):
        if self.max_participants:
            return self.total_registrations >= self.max_participants
        return False


class EventImage(models.Model):
    """Gallery images for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_gallery/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.event.title} - Image {self.id}"


class EventRegistration(models.Model):
    """User event registrations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'event']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.event.title}"
