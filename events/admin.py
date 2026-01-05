from django.contrib import admin
from .models import Event, EventImage, EventRegistration


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'venue', 'status', 'registration_fee', 'total_registrations', 'is_featured']
    list_filter = ['status', 'is_featured', 'date']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventImageInline]
    ordering = ['-date']


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'caption', 'uploaded_at']
    list_filter = ['event', 'uploaded_at']
    search_fields = ['event__title', 'caption']


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at', 'is_active']
    list_filter = ['event', 'is_active', 'registered_at']
    search_fields = ['user__email', 'event__title']
    ordering = ['-registered_at']
