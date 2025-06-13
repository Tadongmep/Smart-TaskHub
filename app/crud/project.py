from sqlalchemy.orm import Session
# Assuming your Project model is in app/models/project.py
from app.models.project_member import ProjectMember
from app.models.project import Project
# Assuming your ProjectCreateRequest schema is in app/schemas/project.py
from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest
import time
from app.api.deps import get_current_user
from app.models.user import User  # Assuming your User model is in app/models/user.py
from fastapi import Depends, HTTPException


def get_project_by_id(db: Session, project_id: int):
    project = db.query(Project).filter(
        Project.id == project_id,
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

def get_projects_list(
    db: Session,
    current_user: User,
    page: int = 1,
    size: int = 10,
    search: str = None
):
    query = db.query(Project).filter(Project.owner_id == current_user.id)

    if search:
        query = query.filter(Project.name.ilike(f"%{search}%"))

    total = query.count()
    projects = query.offset((page - 1) * size).limit(size).all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": projects
    }


def create_project(db: Session, project: ProjectCreateRequest, current_user: User = Depends(get_current_user)):
    current_timestamp = int(time.time())  # Unix timestamp
    db_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id,
        created_at=current_timestamp,
        updated_at=current_timestamp
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project_by_id(
    db: Session, project: ProjectUpdateRequest, current_user: User = Depends(get_current_user)
):
    db_project = get_project_by_id(db, project.id)

    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")

    db_project.name = project.name
    db_project.description = project.description
    db_project.updated_at = int(time.time())

    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project_by_id(
    db: Session, project_id: int, current_user: User = Depends(get_current_user)
):
    db_project = get_project_by_id(db, project_id)

    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")

    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted successfully"}

def add_member_to_project(
    db: Session, project_id: int, email: str, current_user: User = Depends(get_current_user)
):
    db_project = get_project_by_id(db, project_id)

    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add members to this project")

    # Assuming you have a User model and a way to find users by email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    member = ProjectMember(
        project_id=db_project.id,
        user_id=user.id,
        role='member',  # Default role, can be changed as needed
        joined_at=int(time.time())
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    db_project.members.append(member)  # Assuming you have a relationship set up in your Project model
    db.commit()
    db.refresh(db_project)

    return {"detail": f"User {user.email} added to project {db_project.name}"}

def remove_member_from_project(
    db: Session, project_id: int, user_id: int, current_user: User = Depends(get_current_user)
):
    db_project = get_project_by_id(db, project_id)

    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to remove members from this project")

    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == db_project.id,
        ProjectMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found in this project")

    db.delete(member)
    db.commit()
    return {"detail": f"User {user_id} removed from project {db_project.name}"}