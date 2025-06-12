from typing import List, Optional
from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: int
    updated_at: int

    model_config = {
        "from_attributes": True
    }


class ProjectListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[ProjectResponse]


class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int

    model_config = {
        "from_attributes": True
    }


class ProjectUpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ProjectDeleteRequest(BaseModel):
    id: int

    model_config = {
        "from_attributes": True
    }

