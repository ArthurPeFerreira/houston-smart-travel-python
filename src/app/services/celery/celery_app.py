from celery import Celery
from celery.schedules import crontab 
from dotenv import load_dotenv
import os
from datetime import datetime
from src.app.services.seats_aero.seats_aero import fetch_seat_availability

load_dotenv()

REDIS_IP = os.getenv("REDIS_IP")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

celery_app = Celery(
    "celery_app",
    broker=f"redis://{REDIS_IP}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_IP}:{REDIS_PORT}/1"
)

# opções globais do worker / beat
celery_app.conf.update(
    enable_utc=True,  
    timezone="UTC",  
)

celery_app.conf.beat_schedule = {
    "daily-data-update": {
        "task": "src.app.services.celery.celery_app.get_seats_aero_data",
        "schedule": crontab(hour=0, minute=0),
    },
}

celery_app.conf.beat_max_loop_interval = 3600

@celery_app.task
def get_seats_aero_data():
    print(f"Running task at {datetime.now():%Y-%m-%d %H:%M:%S}")
    fetch_seat_availability()
    