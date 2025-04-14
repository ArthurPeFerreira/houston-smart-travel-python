from fastapi import FastAPI
from contextlib import asynccontextmanager

# Função que será executada ao iniciar a API
async def startup_function():
    print("🚀 Servidor FastAPI iniciado!")
    

# Função que será executada ao desligar a API
async def shutdown_function():
    print("❌ Servidor FastAPI desligando...")

# Usando lifespan para configurar eventos de startup e shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_function()
    yield
    await shutdown_function()