from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Iniciar um Worker Linux: celery -A app.workers.celery_app:celery_app worker --loglevel=info --concurrency=4
# Iniciar um Worker Windows: celery -A app.workers.celery_app:celery_app worker --pool=solo --loglevel=info

REDIS_IP = os.getenv("REDIS_IP")
REDIS_PORT = os.getenv("REDIS_PORT")

celery_app = Celery(
    'app',
    broker=f'redis://{REDIS_IP}:{REDIS_PORT}/0',  # Usando Redis como broker
    backend=f'redis://{REDIS_IP}:{REDIS_PORT}/0',  # Backend para armazenar os resultados
    include=['src.app.workers.tasks']  # Lista de módulos com tarefas
)

# Configurações extras
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)