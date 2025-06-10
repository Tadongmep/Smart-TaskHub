from fastapi import FastAPI
from api.route import router

def create_app() -> FastAPI:
    app = FastAPI()

    # Include routes
    app.include_router(router)

    return app

app = create_app()