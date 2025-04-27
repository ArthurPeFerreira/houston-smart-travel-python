import uvicorn
from src.app.api.routes import router
from src.app.api.lifespan import app

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)