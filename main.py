from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, crud, auth, dependencies
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine) # Создание всех таблиц в базе данных на основе моделей

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(SessionLocal), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Получение токена доступа для аутентифицированного пользователя.

    - **db**: Сессия базы данных.
    - **form_data**: Данные формы OAuth2, включающие имя пользователя и пароль.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES) 
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(SessionLocal)):
    db_user = crud.get_user_by_username(db, username=user.username)
    """
    Создание нового пользователя.

    - **user**: Данные пользователя, которые нужно создать.
    - **db**: Сессия базы данных.
    """
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    """
    Получение списка задач текущего пользователя.

    - **db**: Сессия базы данных.
    - **current_user**: Текущий аутентифицированный пользователь.
    """
    tasks = crud.get_tasks(db, user_id=current_user.id)
    return tasks

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user), task_owner: models.Task = Depends(dependencies.get_task_owner)):
    """
    Обновление существующей задачи.

    - **task_id**: Идентификатор задачи, которую нужно обновить.
    - **task**: Новые данные задачи.
    - **db**: Сессия базы данных.
    - **current_user**: Текущий аутентифицированный пользователь.
    - **task_owner**: Задача, принадлежащая текущему пользователю.
    """
    return crud.update_task(db=db, task_id=task_id, task=task)

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user), task_owner: models.Task = Depends(dependencies.get_task_owner)):
    return crud.delete_task(db=db, task_id=task_id)

@app.post("/tasks/{task_id}/permissions", response_model=schemas.TaskPermission)
def create_task_permission(task_id: int, permission: schemas.TaskPermissionCreate, db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user), task_owner: models.Task = Depends(dependencies.get_task_owner)):
    return crud.create_task_permission(db=db, task_id=task_id, permission=permission)

@app.get("/tasks/{task_id}/permissions", response_model=List[schemas.TaskPermission])
def read_task_permissions(task_id: int, db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user), task_owner: models.Task = Depends(dependencies.get_task_owner)):
    return crud.get_task_permissions(db=db, task_id=task_id)
