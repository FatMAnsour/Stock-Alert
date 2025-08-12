from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stock(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.symbol}"

class Alert(models.Model):
    ALERT_TYPES = [
        ('threshold', 'Threshold Alerts'),
        ('duration', 'Duration Alerts'),
    ]
    OPERATORS = [
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('>=', 'Greater Than or Equal'),
        ('<=', 'Less Than or Equal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    operator = models.CharField(max_length=5, choices=OPERATORS)
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    condition_first_met = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.stock.company_name} - {self.alert_type}"

class TriggeredAlert(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    triggered_at = models.DateTimeField(auto_now_add=True)
    stock_price_at_trigger = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    
    def __str__(self):
        return f"Alert triggered: {self.alert.stock.symbol} at {self.triggered_at}"