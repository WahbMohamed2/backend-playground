from pydantic import BaseModel, ConfigDict, field_validator
from typing import Literal, Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        # Why: strips whitespace first, then checks if anything is left
        # "   " would pass a simple `if not v` check — this catches it
        if not v.strip():
            raise ValueError("Title cannot be blank or whitespace")
        return v.strip()  # also cleans the value before saving it

class TaskUpdate(BaseModel):
    # Why all Optional: PATCH-style updates let the client send only what changed
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: Optional[datetime]
    created_at: datetime
    owner_id: int

    # Why: SQLAlchemy returns objects with attributes (task.title)
    # not dictionaries (task["title"]) — this tells Pydantic to handle both
    model_config = ConfigDict(from_attributes=True)