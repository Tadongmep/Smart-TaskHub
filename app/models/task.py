from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.db import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # e.g., enum: 'todo', 'doing', 'done'
    status = Column(String, nullable=False)
    # e.g., enum: 'low', 'medium', 'high'
    piority = Column(String, nullable=False)
    due_date = Column(Integer, nullable=True)  # Unix timestamp for due date
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"),
                         nullable=True)  # Nullable if not assigned
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="tasks", foreign_keys=[project_id])
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")
    created_user = relationship("User", back_populates="task_creator" ,foreign_keys=[created_by])
    assigned_user = relationship("User", back_populates="assignee", foreign_keys=[assigned_to])

    def __repr__(self):
        return f"<Task(id={self.id}, project_id={self.project_id}, title={self.title}, status={self.status})>"

    def __str__(self):
        return f"Task(id={self.id}, project_id={self.project_id}, title={self.title}, status={self.status})"

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "piority": self.piority,
            "due_date": self.due_date,
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
