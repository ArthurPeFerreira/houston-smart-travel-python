from fastapi import FastAPI
import uvicorn
from src.app.api.lifespan import lifespan
from src.app.api.routes import router

app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)