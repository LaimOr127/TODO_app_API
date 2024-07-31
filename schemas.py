from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class TaskPermissionCreate(BaseModel):
    user_id: int
    can_read: bool = False
    can_update: bool = False

class TaskPermission(BaseModel):
    id: int
    task_id: int
    user_id: int
    can_read: bool
    can_update: bool

    class Config:
        orm_mode = True
