from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user
from . import crud, models

# Функция для получения владельца задачи, которая проверяет, имеет ли текущий пользователь доступ к задаче
def get_task_owner(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Вложенная функция, которая проверяет, является ли текущий пользователь владельцем задачи
    def inner(task_id: int):
        # Получаем задачу по ID из базы данных
        task = crud.get_task(db, task_id)
        if task is None or task.owner_id != current_user.id:
            # Если задача не существует или пользователь не является владельцем, возвращаем ошибку
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return task
    # Возвращаем вложенную функцию, которая будет использоваться для проверки доступа
    return inner
