from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import atexit

scheduler = None

def stock_update_job():
    """Job function that runs periodically"""
    from .stock_service import StockService
    service = StockService()
    service.update_all_prices()

def start_scheduler():
    """Start the background scheduler"""
    global scheduler
    
    if scheduler is None:
        scheduler = BackgroundScheduler()
        
        # Schedule job every 15 minutes
        scheduler.add_job(
            stock_update_job,
            'interval',
            minutes=15,
            id='stock_update_job',
            replace_existing=True
        )
        
        scheduler.start()
        print("Scheduler started - will check stocks every 15 minutes")
        
        # Shut down scheduler on exit
        atexit.register(lambda: scheduler.shutdown())
