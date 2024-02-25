"""
test_app.py
DOCUMENTATION
LICENSE: ALL RIGHTS RESERVED

Tutorial based on:
PyTest • REST API Integration Testing with Python
https://www.youtube.com/watch?v=7dgQRVqF1N0
"""

import os
import requests
from icecream import ic
import uuid

os.system("cls")

ENDPOINT = r"https://todo.pixegami.io"

# Verify this works.
response = requests.get(ENDPOINT)
# ic(response)

data = response.json()
# ic(data)

status_code = response.status_code
# ic(status_code)


def test_can_call_the_endpoint():
    # HTTPS Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    # SEND PAYLOAD TASK
    payload = new_task_payload()
    response_create_task = send_new_task(payload)
    assert response_create_task.status_code == 200

    # VERIFY tas sent
    data_create_task = response_create_task.json()
    id_create_task = data_create_task["task"]["task_id"]
    response_get_task = req_get_task(id_create_task)
    assert response_get_task.status_code == 200

    data_get_task = response_get_task.json()
    assert payload["content"] == data_get_task["content"]
    assert payload["user_id"] == data_get_task["user_id"]


class me:

    def test_can_get_task():
        test_can_create_task()


def test_can_update_task():

    # ** create a task
    payload = new_task_payload()
    response_create_task = send_new_task(payload)
    assert response_create_task.status_code == 200
    task_id = response_create_task.json()["task"]["task_id"]

    # ** update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True,
    }
    response_update_task = send_update_task(new_payload)
    assert response_update_task.status_code == 200

    # ** get and validate the changes
    response_get_task = req_get_task(task_id)
    assert response_get_task.status_code == 200
    data_get_task = response_get_task.json()
    # ic(data_get_task)
    assert new_payload["user_id"] == data_get_task["user_id"]
    assert new_payload["content"] == data_get_task["content"]
    assert new_payload["is_done"] == data_get_task["is_done"]

    # data_update_task = response_update_task.json()
    # ic(data_update_task)
    # assert data_update_task["content"] == new_payload["content"]
    # assert data_update_task["user_id"] == new_payload["user_id"]
    # assert data_update_task["user_id"] == new_payload["user_id"]


def test_can_list_tasks():
    # create 3 tasks
    # list tasks, get 3 items back.
    # Don't check content, Test 1 checks content.
    N = 3
    payload = new_task_payload()
    for _ in range(N):
        response_create_task = send_new_task(payload)
        assert response_create_task.status_code == 200

    response_list_task = req_list_task(payload["user_id"])
    # response_list_task = req_list_task("test_user")
    assert response_list_task.status_code == 200
    data_list_tasks = response_list_task.json()

    tasks = data_list_tasks["tasks"]
    assert len(tasks) == N
    # ic(data_list_tasks)


def test_can_delete_task():
    # create it
    # delete it
    # assert error - task doesn't exist.
    payload = new_task_payload()
    response_create_task = send_new_task(payload)
    assert response_create_task.status_code == 200

    # GET Task Sent
    id_create_task = response_create_task.json()["task"]["task_id"]
    # Delete Task
    response_delete_task = req_delete_task(id_create_task)
    assert response_delete_task.status_code == 200

    response_get_task = req_get_task(id_create_task)
    assert response_get_task.status_code == 404


def send_new_task(payload_to_send):
    return requests.put(ENDPOINT + "/create-task", json=payload_to_send)


def req_get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def send_update_task(payload_to_send):
    return requests.put(ENDPOINT + "/update-task", json=payload_to_send)


def req_list_task(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def req_delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}\n"
    content = f"text_content_{uuid.uuid4().hex}\n"

    # print(f"Creating task for us :\n{user_id} \nwith content: \n{content}\n")

    return {
        "content": content,
        "user_id": user_id,
        # "task_id": "test_task_id",  # Don't need to pass task ID. ID is generated Server-Side.
        "is_done": False,
    }
