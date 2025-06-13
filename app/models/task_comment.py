from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.db import Base
from sqlalchemy.orm import relationship

class TaskComment(Base):
    __tablename__ = "task_comments"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False)

    # Relationships
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments", foreign_keys=[user_id])

    def __repr__(self):
        return f"<TaskComment(id={self.id}, task_id={self.task_id}, user_id={self.user_id})>"

    def __str__(self):
        return f"TaskComment(id={self.id}, task_id={self.task_id}, user_id={self.user_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at
        }
