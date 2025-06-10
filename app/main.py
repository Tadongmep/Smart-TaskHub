from fastapi import FastAPI
from api.route import router
from core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json")

    # Include routes
    app.include_router(router, prefix=settings.API_V1_STR)

    return app

app = create_app()