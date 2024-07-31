from uuid import uuid4
import requests


ENDPOINT = "(Пример/http://127.0.0.1:8000)" # Базовый URL для вашего API


def test_can_put_and_get_task():
    user_id = f"user_{uuid4().hex}"
    random_task_content = f"task content: {uuid4().hex}"
    create_response = create_task(user_id, random_task_content)
    assert create_response.status_code == 200

    task_id = create_response.json()["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    print(get_task_response)
    assert get_task_response.json()["content"] == random_task_content


def test_can_list_tasks():
    # Создайте нового пользователя для этого теста.
    user_id = f"user_{uuid4().hex}"

    # Создайте 3 задачи для этого пользователя.
    for i in range(3):
        create_task(user_id, f"task_{i}")

    # Перечислите задачи для этого пользователя.
    response = list_tasks(user_id)
    tasks = response.json()["tasks"]
    assert len(tasks) == 3


def test_can_update_task():
    # Создайте нового пользователя для этого теста.
    user_id = f"user_{uuid4().hex}"
    create_response = create_task(user_id, "task content")
    task_id = create_response.json()["task"]["task_id"]

    # Обновите задачу новым содержимым.
    new_task_content = f"updated task content: {uuid4().hex}"
    payload = {
        "content": new_task_content,
        "task_id": task_id,
        "is_done": True,
    }
    update_task_response = update_task(payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    assert get_task_response.json()["content"] == new_task_content
    assert get_task_response.json()["is_done"] == True


def test_can_delete_task():
    user_id = f"user_{uuid4().hex}"
    create_response = create_task(user_id, "task1")
    task_id = create_response.json()["task"]["task_id"]

    # Удалить задачу.
    delete_task(task_id)

    # Мы больше не сможем получить задание.
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def list_tasks(user_id: str) -> dict:
    return requests.get(f"{ENDPOINT}/list-tasks/{user_id}")

    """
    Получить список задач для заданного пользователя.

    :param user_id: Идентификатор пользователя
    :return: Словарь с ответом от сервера, содержащий список задач
    """

def create_task(user_id: str, content: str) -> dict:

    """
    Создать новую задачу для заданного пользователя.

    :param user_id: Идентификатор пользователя
    :param content: Содержимое задачи
    :return: Словарь с ответом от сервера, содержащий информацию о созданной задаче
    """

    payload = {
        "user_id": user_id,
        "content": content,
    }
    return requests.put(f"{ENDPOINT}/create-task", json=payload)


def get_task(task_id: str) -> dict: #  Получить информацию о задаче по её идентификатору.
    return requests.get(f"{ENDPOINT}/get-task/{task_id}")


def delete_task(task_id: str) -> dict: # Удалить задачу по её идентификатору.
    return requests.delete(f"{ENDPOINT}/delete-task/{task_id}")


def update_task(payload: dict) -> dict: # Обновить существующую задачу.
    return requests.put(f"{ENDPOINT}/update-task", json=payload)
