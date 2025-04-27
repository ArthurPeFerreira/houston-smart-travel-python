from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.app.api.lifespan import app
from src.app.services.celery.celery_app import celery_app, get_seats_aero_data

router = APIRouter()

@router.get("/")
async def home():
    return {"status": "Servidor rodando!"}

@router.get("/status")
def status():
    """Retorna saúde do worker, beat e broker."""
    # 1) processos vivos?
    worker_alive = app.state.worker.poll() is None
    beat_alive   = app.state.beat.poll()   is None

    # 2) ping Celery (timeout 1 s)
    try:
        ping = celery_app.control.ping(timeout=1.0)
        broker_ok = bool(ping)
    except Exception:
        broker_ok = False

    return {
        "worker": "online" if worker_alive else "offline",
        "beat":   "online" if beat_alive   else "offline",
        "broker": "ok"     if broker_ok    else "error",
        "detail": ping if broker_ok else [],
    }

@router.get("/update")
def update():
    """Atualiza os dados de assentos."""
    get_seats_aero_data.delay()   
    return {"status": "Update requested!"}


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")