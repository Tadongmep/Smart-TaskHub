from sqlalchemy import Column, Integer, String
from core.db import Base
from sqlalchemy import ForeignKey

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"

    def __str__(self):
        return f"User(id={self.id}, email={self.email}, full_name={self.full_name})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }