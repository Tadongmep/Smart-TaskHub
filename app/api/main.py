from fastapi import APIRouter

from app.api.routes import auth, user, project

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to FastAPI with Factory Pattern"}

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/user", tags=["user"])
router.include_router(project.router, prefix="/project", tags=["project"])