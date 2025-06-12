from fastapi import APIRouter

from api.routes import auth, user

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to FastAPI with Factory Pattern"}

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/user", tags=["user"])