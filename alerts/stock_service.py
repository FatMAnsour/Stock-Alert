import requests
import time
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Stock, Alert, TriggeredAlert

class StockService:
    def __init__(self):
        self.api_key = settings.STOCK_API_KEY
        self.base_url = "https://api.twelvedata.com"
        
        # Predefined stocks
        self.predefined_stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation'},
            {'symbol': 'NFLX', 'name': 'Netflix Inc.'},
            {'symbol': 'AMD', 'name': 'Advanced Micro Devices'},
            {'symbol': 'PYPL', 'name': 'PayPal Holdings Inc.'},
        ]
    
    def initialize_stocks(self):
        """Create stock entries if they don't exist"""
        for stock_data in self.predefined_stocks:
            Stock.objects.get_or_create(
                symbol=stock_data['symbol'],
                defaults={'company_name': stock_data['name']}
            )
        print("Stocks initialized")
    
    def fetch_stock_price(self, symbol):
        """Fetch price for single stock"""
        try:
            url = f"{self.base_url}/price"
            params = {'symbol': symbol, 'apikey': self.api_key}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    return float(data['price'])
            
            print(f" Failed to fetch {symbol}")
            return None
                
        except Exception as e:
            print(f" Error fetching {symbol}: {e}")
            return None
    
    def update_all_prices(self):
        """Update all stock prices"""
        stocks = Stock.objects.all()
        updated = 0
        
        for stock in stocks:
            price = self.fetch_stock_price(stock.symbol)
            if price:
                stock.current_price = price
                stock.save()
                updated += 1
                print(f"{stock.symbol}: ${price}")
            time.sleep(8)  # Rate limiting
        
        print(f"Updated {updated}/{stocks.count()} stocks")
        self.process_alerts()  # Check alerts after updating prices
        return updated
    
    def check_alert_condition(self, alert):
        """Check if alert condition is met"""
        current_price = alert.stock.current_price
        if not current_price:
            return False
            
        if alert.operator == '>':
            return current_price > alert.threshold_price
        elif alert.operator == '<':
            return current_price < alert.threshold_price
        elif alert.operator == '>=':
            return current_price >= alert.threshold_price
        elif alert.operator == '<=':
            return current_price <= alert.threshold_price
        
        return False
    
    def process_alerts(self):
        """Process all active alerts"""
        active_alerts = Alert.objects.filter(is_active=True)
        triggered = 0
        
        for alert in active_alerts:
            try:
                condition_met = self.check_alert_condition(alert)
                
                if alert.alert_type == 'threshold' and condition_met:
                    self.trigger_alert(alert)
                    triggered += 1
                
                elif alert.alert_type == 'duration':
                    if condition_met:
                        now = timezone.now()
                        if not alert.condition_first_met:
                            alert.condition_first_met = now
                            alert.save()
                        else:
                            duration_passed = now - alert.condition_first_met
                            if duration_passed >= timedelta(hours=alert.duration_hours):
                                self.trigger_alert(alert)
                                triggered += 1
                    else:
                        # Reset duration tracking if condition not met
                        alert.condition_first_met = None
                        alert.save()
                        
            except Exception as e:
                print(f" Error processing alert {alert.id}: {e}")
        
        if triggered > 0:
            print(f"{triggered} alerts triggered")
        return triggered
    
    def trigger_alert(self, alert):
        """Trigger alert and send notification"""
        current_price = alert.stock.current_price
        message = f"STOCK ALERT: {alert.stock.symbol} is {alert.operator} ${alert.threshold_price}. Current price: ${current_price}"
        
        # Create record
        TriggeredAlert.objects.create(
            alert=alert,
            stock_price_at_trigger=current_price,
            message=message
        )
        
        # Send notification
        self.send_notification(alert, message)
        
        # Deactivate to prevent spam
        alert.is_active = False
        alert.save()
    
    def send_notification(self, alert, message):
        """Send email or console notification"""
        try:
            if alert.user.email and settings.EMAIL_HOST_USER:
                send_mail(
                    subject=f"Stock Alert: {alert.stock.symbol}",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[alert.user.email],
                    fail_silently=False,
                )
                print(f"Email sent to {alert.user.email}")
            else:
                print(f"{message}")
        except Exception as e:
            print(f" Email failed: {e}")
            print(f"{message}")