from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.crud.project import add_member_to_project, create_project, get_project_by_id, get_projects_list, remove_member_from_project, update_project_by_id, delete_project_by_id
from app.models.project import Project
from app.models.user import User
from app.core.db import get_db
from app.schemas.project import ProjectAddMemberRequest, ProjectCreateRequest, ProjectListResponse, ProjectResponse, ProjectUpdateRequest
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
    projects = get_projects_list(db, current_user, page, size, search)

    return ProjectListResponse(
        total=projects['total'],
        page=projects['page'],
        size=projects['size'],
        items=projects['items']
    )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.post("/create-project", response_model=ProjectResponse)
async def create_prject(
    request: ProjectCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_project = db.query(Project).filter(
        Project.name == request.name,
        Project.owner_id == current_user.id
    ).first()

    if existing_project:
        raise HTTPException(
            status_code=400, detail="Project with this name already exists")

    new_project = create_project(db, request, current_user)
    if not new_project:
        raise HTTPException(status_code=500, detail="Failed to create project")

    return new_project


@router.post("/update-project", response_model=ProjectResponse)
async def update_project(
    request: ProjectUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = update_project_by_id(db, request, current_user)

    return project


@router.delete("/delete-project/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = delete_project_by_id(db, project_id, current_user)

    return project


@router.post("/project-add-user/{project_id}")
async def add_user_to_project(
    project_id: int,
    user_email: ProjectAddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = add_member_to_project(
        db, project_id, user_email.email, current_user)
    if not result:
        raise HTTPException(
            status_code=404, detail="Project not found or user not added")
    return result


@router.delete("/project-remove-user/{project_id}/{user_id}")
async def remove_user_from_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = remove_member_from_project(
        db, project_id, user_id, current_user)

    return result
