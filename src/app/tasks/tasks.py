from src.app.tasks.celery_app import celery_app  # Importa a instância do Celery

# Task de agendamento: lê os clientes do Redis e dispara a task individual para cada um.
@celery_app.task
def process_clients():    
    print("📅 Executando tarefa agendada via CRON")
