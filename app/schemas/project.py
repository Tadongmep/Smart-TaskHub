from typing import List, Optional
from pydantic import BaseModel

from app.schemas.user import UserShortResponse


class ProjectListRequest(BaseModel):
    page: int = 1
    size: int = 10
    search: Optional[str] = None


class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectDeleteRequest(BaseModel):
    id: int


class ProjectAddMemberRequest(BaseModel):
    email: str


class ProjectMemberResponse(BaseModel):
    id: int
    role: str
    joined_at: int
    user_information: UserShortResponse  # 🔁 Nested user

    model_config = {"from_attributes": True}


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: int
    updated_at: int
    members: list[ProjectMemberResponse] = []

    model_config = {
        "from_attributes": True
    }


class ProjectListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[ProjectResponse]


class ProjectRemoveMemberRequest(BaseModel):
    project_id: str
    user_id: str
