from sqlalchemy.orm import Session
# Assuming your Project model is in app/models/project.py
from models.project import Project
# Assuming your ProjectCreateRequest schema is in app/schemas/project.py
from schemas.project import ProjectCreateRequest
import time
from api.deps import get_current_user
from models.user import User  # Assuming your User model is in app/models/user.py
from fastapi import Depends


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
