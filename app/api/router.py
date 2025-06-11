from fastapi import APIRouter

# from app.api.routes import auth

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to FastAPI with Factory Pattern"}

# router.include_router(auth.router, prefix="/auth", tags=["auth"])