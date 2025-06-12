from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user
from models.project import Project
from models.user import User
from core.db import get_db
from schemas.project import ProjectCreateRequest, ProjectListResponse, ProjectResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/projects", response_model=ProjectListResponse)
async def get_projects(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Project).filter(Project.owner_id == current_user.id)

    if search:
        query = query.filter(Project.name.ilike(f"%{search}%"))

    total = query.count()
    projects = query.offset((page - 1) * size).limit(size).all()

    return ProjectListResponse(
        total=total,
        page=page,
        size=size,
        items=projects
    )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.post("/create-project", response_model=ProjectResponse)
async def create_prject(
    request: ProjectCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass