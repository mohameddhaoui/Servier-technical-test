from lib.modules.data_transformation.data_processing import (
    run_mentions_collection_pipeline,
)
from lib.helpers.logger import logger


def run_data_transformation(data_prep_output: dict) -> dict:
    """
    Run data transformation pipeline
        Params:
        --------
             data_prep_output (dict) : preprocessed files paths

        Returns:
        ---------
             data_processing_output (dict) : A dictionary containing the quality check operations result

    """
    logger.info(f"-:----------- Run mention collection and processing  -:-")
    data_transformation_output = run_mentions_collection_pipeline(data_prep_output)
    logger.info(data_transformation_output)

    return data_transformation_output
