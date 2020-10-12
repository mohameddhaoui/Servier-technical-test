from config import SUCCESS_STATUS


def is_success(task_result: dict) -> bool:
    """
    Transform task result to bool
    """
    return task_result["task_status"] == SUCCESS_STATUS


def generate_task_result(task_id="", task_status="", task_result="") -> dict:
    """
    Generate task result as dict
    """
    return {"task_id": task_id, "task_status": task_status, "task_result": task_result}
