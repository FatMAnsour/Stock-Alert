from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Alert, TriggeredAlert

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    stock_name = serializers.ReadOnlyField(source='stock.company_name')
    stock_symbol = serializers.ReadOnlyField(source='stock.symbol')
    class Meta:
        model = Alert
        fields = ['id', 'stock', 'stock_name', 'stock_symbol', 'alert_type', 'operator', 'threshold_price',
                   'duration_hours', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class TriggeredAlertSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.ReadOnlyField(source='alert.stock.symbol')
    alert_description = serializers.SerializerMethodField()
    
    class Meta:
        model = TriggeredAlert
        fields = ['id', 'triggered_at', 'stock_price_at_trigger', 'message',
                  'stock_symbol', 'alert_description']
    
    def get_alert_description(self, obj):
        return f"{obj.alert.stock.symbol} {obj.alert.operator} {obj.alert.threshold_price}"


    
