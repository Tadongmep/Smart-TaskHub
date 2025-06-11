from sqlalchemy import Column, Integer, String
from core.db import Base
from sqlalchemy import ForeignKey


class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # e.g., 'admin', 'member', etc.
    # Timestamp of when the user joined the project
    joined_at = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ProjectMember(id={self.id}, project_id={self.project_id}, user_id={self.user_id}, role={self.role})>"

    def __str__(self):
        return f"ProjectMember(id={self.id}, project_id={self.project_id}, user_id={self.user_id}, role={self.role})"

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "role": self.role,
            "joined_at": self.joined_at
        }
