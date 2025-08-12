from django.core.management.base import BaseCommand
from alerts.stock_service import StockService

class Command(BaseCommand):
    help = 'Manually update stock prices'
    
    def handle(self, *args, **options):
        service = StockService()
        updated = service.update_all_prices()
        self.stdout.write(
            self.style.SUCCESS(f'Updated {updated} stocks')
        )