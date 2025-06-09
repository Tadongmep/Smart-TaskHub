from fastapi import FastAPI
from app.api.route import router
from app.db.session import engine, Base

def create_app() -> FastAPI:
    app = FastAPI()

    # Create DB tables
    Base.metadata.create_all(bind=engine)

    # Include routes
    app.include_router(router)

    return app

app = create_app()