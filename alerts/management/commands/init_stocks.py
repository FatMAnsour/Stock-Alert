from django.core.management.base import BaseCommand
from alerts.stock_service import StockService

class Command(BaseCommand):
    help = 'Initialize predefined stocks'
    
    def handle(self, *args, **options):
        service = StockService()
        service.initialize_stocks()
        self.stdout.write(self.style.SUCCESS('Stocks initialized'))