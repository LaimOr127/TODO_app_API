from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    Модель пользователя.
    Таблица `users` хранит информацию о пользователях системы.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Task(Base):
    """
    Модель задачи.
    Таблица `tasks` хранит информацию о задачах, принадлежащих пользователям.
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

class TaskPermission(Base):
    """
    Модель разрешений на задачи.
    Таблица `task_permissions` хранит информацию о разрешениях пользователей на задачи.
    """
    __tablename__ = "task_permissions"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    can_read = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    task = relationship("Task")
    user = relationship("User")
