import os

def start_woker():
    os.system("celery -A src.app.tasks.celery_app:celery_app worker --pool=solo --loglevel=info")    
    