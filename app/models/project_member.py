from sqlalchemy import Column, Integer, String
from app.core.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # e.g., 'admin', 'member', etc.
    # Timestamp of when the user joined the project
    joined_at = Column(Integer, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="members")
    user_information = relationship("User", back_populates="memberships")

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
