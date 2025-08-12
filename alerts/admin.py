from django.contrib import admin
from .models import Stock, Alert, TriggeredAlert

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company_name', 'current_price', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['symbol', 'company_name']
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'alert_type', 'operator', 'threshold_price', 'is_active']
    list_filter = ['alert_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'stock__symbol']

@admin.register(TriggeredAlert)
class TriggeredAlertAdmin(admin.ModelAdmin):
    list_display = ['alert', 'triggered_at', 'stock_price_at_trigger']
    list_filter = ['triggered_at']