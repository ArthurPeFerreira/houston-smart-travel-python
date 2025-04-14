from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.app.tasks.worker import start_woker

router = APIRouter()

@router.get("/")
async def home():
    return {"status": "Servidor rodando!"}

@router.get("/teste")
async def teste():
    start_woker()
    return {"status": "Testado!"}

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")