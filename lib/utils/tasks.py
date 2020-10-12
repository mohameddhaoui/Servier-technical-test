from config import SUCCESS_STATUS

def is_success(task_result):
    return task_result["task_status"]== SUCCESS_STATUS


def generate_task_result( task_id="", task_status="", task_result=""):
    return {"task_id":task_id, "task_status":task_status,"task_result":task_result}