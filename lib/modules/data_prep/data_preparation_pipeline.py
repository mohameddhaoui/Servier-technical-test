
from lib.modules.data_prep.data_retrieval import run_data_retrieval
from lib.modules.data_prep.data_quality import run_data_quality_pipeline
from lib.modules.data_prep.data_preprocessing import run_data_preprocessing_pipeline
from lib.utils.file import load_datasrc_config
from lib.modules.data_transfer.move_file import run_move_file
from config import PREPROCESSED_ZONE_DIRECTORY, QUARANTINE_ZONE_DIRECTORY


def run_data_prep(list_data_src: list)-> dict:
    """
    Run data preparation_pipeline for all datasources
        Params:
        --------
             list_data_src (list) : a list of datasource names (str)

        Returns:
        ---------
             data_preparation_output (dict) : contains preprocessed files paths for each datasource
    """
    data_preparation_output = {}
    for datasrc_name in list_data_src :
        config_datasrc = load_datasrc_config(datasrc_name)
        output_dataprep= run_datasrc_dataprep_pipeline(config_datasrc)
        data_preparation_output[datasrc_name]=output_dataprep["output_filepath"]
    return data_preparation_output

def run_datasrc_dataprep_pipeline(config_datasrc:dict)-> dict:
    """
    Run Data prep pipeline for a given datasrc :
        - retrieve files
        - move to quarantine zone
        - run quality checks
        - run preprocessings pipeline

        Params:
        --------
             config_datasrc (dict) : a datasource config

        Returns:
        ---------
             result (dict) : contains preprocessed files paths and raw data paths

    """
    config_data_retrieval = config_datasrc["datasource"]["pipeline"]["data_collection"]

    print("running data retrieval")
    data_retrieval_result = run_data_retrieval(config_data_retrieval)

    print("move file to quarantine")
    move_to_quarantine_result = run_move_file(source_path= data_retrieval_result["task_result"], destination_zone=QUARANTINE_ZONE_DIRECTORY, dependency=data_retrieval_result)

    print("run quality check")
    #print(move_to_quarantine_result)
    dataquality_config = config_datasrc["datasource"]["pipeline"]["data_quality"]
    data_quality_result = run_data_quality_pipeline(move_to_quarantine_result["task_result"], dataquality_config, dependency=move_to_quarantine_result)

    print("run data preprocessing")
    data_preprocessing_config = config_datasrc["datasource"]["pipeline"]["data_preprocessing"]
    output_preprocessed_filepath = run_data_preprocessing_pipeline(move_to_quarantine_result["task_result"], config_datasrc["datasource"]["name"], data_preprocessing_config,output_directory=PREPROCESSED_ZONE_DIRECTORY,
                                                      dependency= data_quality_result )

    return {"output_filepath":output_preprocessed_filepath["task_result"], "raw_file_path":move_to_quarantine_result["task_result"]}





if __name__ == "__main__":
    data_preparation_output = run_data_prep(["drugs"])
    print(data_preparation_output)
