import subprocess, signal, os
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
import asyncio

def _spawn(cmd: list[str]) -> subprocess.Popen:
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    return subprocess.Popen(cmd, creationflags=flags)

# Função que será executada ao iniciar a API
async def startup_function():
    print("🚀 Servidor FastAPI iniciado!")

    # ------ define comandos de acordo com o SO ------
    worker_cmd = ["celery", "-A", "src.app.services.celery.celery_app", "worker", "-l", "info"]
    if os.name == "nt":          # Windows → threads
        worker_cmd += ["-P", "threads", "-c", "8"]
    else:                        # Linux/macOS → pool default (prefork) c/ 4 proc
        worker_cmd += ["-c", "4"]

    app.state.worker = _spawn(worker_cmd)

    await asyncio.sleep(30)

    app.state.beat   = _spawn(
        ["celery", "-A", "src.app.services.celery.celery_app", "beat", "-l", "info"]
    )

# Função que será executada ao desligar a API
async def shutdown_function():
    print("❌ Servidor FastAPI desligando...")

    for proc in (app.state.beat, app.state.worker):
        if proc.poll() is None:  # ainda vivo?
            if os.name == "nt":
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                proc.terminate()             # SIGTERM
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()                  # SIGKILL se travar

# Usando lifespan para configurar eventos de startup e shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_function()
    yield
    await shutdown_function()

app = FastAPI(lifespan=lifespan)   