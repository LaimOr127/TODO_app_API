import os
import time
import boto3
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key

app = FastAPI() # Создаем экземпляр FastAPI
handler = Mangum(app) # Создаем Mangum handler для работы с AWS Lambda


class PutTaskRequest(BaseModel): # Модель данных для создания и обновления задач
    content: str
    user_id: Optional[str] = None
    task_id: Optional[str] = None
    is_done: bool = False


@app.get("/") # Корневой маршрут для проверки работы API
async def root():
    return {"message": "Привет в ToDo API!"}


@app.put("/create-task") # Маршрут для создания новой задачи
async def create_task(put_task_request: PutTaskRequest):
    created_time = int(time.time()) #Время в секундах
    item = { #Формирование элемента
        "user_id": put_task_request.user_id,
        "content": put_task_request.content,
        "is_done": False,
        "created_time": created_time,
        "task_id": f"task_{uuid4().hex}",
        "ttl": int(created_time + 86400),  # Срок действия истекает через 24 часа.
    }

    # Поместите это в таблицу.
    table = _get_table()
    table.put_item(Item=item)
    return {"task": item}


@app.get("/get-task/{task_id}") # Маршрут для получения задачи по её идентификатору
async def get_task(task_id: str):
    # Берем задание из таблицы.
    table = _get_table()
    response = table.get_item(Key={"task_id": task_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return item 


@app.get("/list-tasks/{user_id}") # Маршрут для получения списка задач пользователя
async def list_tasks(user_id: str):
    
    # Перечислите N лучших задач из таблицы, используя индекс пользователя.
    table = _get_table()
    response = table.query(
        IndexName="user-index",
        KeyConditionExpression=Key("user_id").eq(user_id),
        ScanIndexForward=False,
        Limit=10, # Ограничение на количество возвращаемых задач
    )
    tasks = response.get("Items")
    return {"tasks": tasks}


@app.put("/update-task") # Маршрут для обновления задачи
async def update_task(put_task_request: PutTaskRequest):
    # Обновляем задачу в таблице.
    table = _get_table()
    table.update_item(
        Key={"task_id": put_task_request.task_id},
        UpdateExpression="SET content = :content, is_done = :is_done",
        ExpressionAttributeValues={
            ":content": put_task_request.content,
            ":is_done": put_task_request.is_done,
        },
        ReturnValues="ALL_NEW", # Возвращаем обновленный элемент
    )
    return {"updated_task_id": put_task_request.task_id}


@app.delete("/delete-task/{task_id}") # Маршрут для удаления задачи по её идентификатору
async def delete_task(task_id: str):
    # Удаляем задачу из таблицы.
    table = _get_table()
    table.delete_item(Key={"task_id": task_id})
    return {"deleted_task_id": task_id}


def _get_table(): #Вспомогательная функция
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)
