from sqlalchemy import Column, Integer, String
from app.core.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    # Relationships
    owned_projects = relationship("Project", back_populates="owner")
    memberships = relationship("ProjectMember", back_populates="user_information")
    comments = relationship("TaskComment", back_populates="user")
    task_creator = relationship("Task", back_populates="created_user", foreign_keys="Task.created_by")
    assignee = relationship("Task", back_populates="assigned_user", foreign_keys="Task.assigned_to")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"

    def __str__(self):
        return f"User(id={self.id}, email={self.email}, full_name={self.full_name})"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }