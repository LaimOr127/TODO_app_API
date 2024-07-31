from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Настройка контекста для хеширования паролей

def get_user(db: Session, user_id: int): # Функция для получения пользователя по ID
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str): # Функция для получения пользователя по имени пользователя
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password) # Хешируем пароль
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user) # Добавляем пользователя в сессию
    db.commit()
    db.refresh(db_user)  # Обновляем объект пользователя
    return db_user

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id) # Создаем объект задачи
    db.add(db_task)  # Добавляем задачу в сессию
    db.add(db_task)
    db.commit() # Фиксируем изменения
    db.refresh(db_task)  # Обновляем объект задачи
    return db_task

def get_tasks(db: Session, user_id: int): # Функция для получения всех задач пользователя
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def get_task(db: Session, task_id: int): # Функция для получения задачи по ID
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = get_task(db, task_id) # Получаем задачу по ID
    if db_task:
        for key, value in task.dict().items():  # Обновляем атрибуты задачи
            setattr(db_task, key, value) 
        db.commit()
        db.refresh(db_task) # Обновляем объект задачи
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task) # Удаляем задачу из сессии
        db.commit()
    return db_task

def create_task_permission(db: Session, task_id: int, permission: schemas.TaskPermissionCreate):
    db_permission = models.TaskPermission(task_id=task_id, **permission.dict())
    db.add(db_permission) # Добавляем разрешение в сессию
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_task_permissions(db: Session, task_id: int): # Функция для получения всех разрешений на задачу
    return db.query(models.TaskPermission).filter(models.TaskPermission.task_id == task_id).all()
