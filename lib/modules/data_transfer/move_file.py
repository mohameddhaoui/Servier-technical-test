import os
import shutil
from lib.utils.tasks import generate_task_result, is_success
from config import SUCCESS_STATUS

def run_move_file(source_path, destination_zone, dependency):

    if is_success(dependency) :
        try:
            if (source_path[0] != "/"):
                source_path=f"/{source_path}"
            filename=os.path.basename(source_path)
            target_zone_filepath= f"{destination_zone}{filename}"
            shutil.copyfile(f".{source_path}",target_zone_filepath)
            task_status =SUCCESS_STATUS #  return {"task_status":target_zone_filepath}
        except Exception as e:
                task_status = e
    return  generate_task_result(task_id="move_file", task_status=task_status, task_result=target_zone_filepath)
