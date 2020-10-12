
import re
import os
from config import SUCCESS_STATUS
from lib.utils.tasks import generate_task_result

def run_data_retrieval(config_data_retrieval):
    task_status = SUCCESS_STATUS
    try :
        datasrc_files_directory = config_data_retrieval["file_path"]
        regex_filename = config_data_retrieval['filename']
        list_datasrc_files_path = get_data_source_files_path(datasrc_files_directory, regex_filename )
        retrieved_paths = list_datasrc_files_path[0] # here we suppose we have only one file for each datasrc
    except Exception as e:
        task_status = e
    return generate_task_result(task_id="data_retrieval",task_status=task_status, task_result=retrieved_paths)


def get_data_source_files_path(datasrc_directory, regex_filename):
    list_all_files_directory = os.listdir(datasrc_directory)
    datasrc_regex_files = [f"{datasrc_directory}{file_name}"
                           for file_name in list_all_files_directory if re.match(regex_filename, file_name)]
    return datasrc_regex_files