from app.database import Base
from app.models.user import User
from app.models.task import Task

# This makes it easier to import all models at once elsewhere
__all__ = ["Base", "User", "Task"]