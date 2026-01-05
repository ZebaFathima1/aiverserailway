from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'amount', 'status', 'transaction_id', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'event']
    search_fields = ['user__email', 'transaction_id', 'user__full_name']
    readonly_fields = ['submitted_at', 'processed_at']
    ordering = ['-submitted_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'event', 'processed_by')
