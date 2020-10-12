
from config import LIST_DATASRC
from lib.helpers.logger import logger
from lib.modules.data_prep.data_preparation_pipeline import run_data_prep
from lib.modules.data_transformation.data_transformation_pipeline import run_data_transformation
from lib.modules.data_exposition.data_exposition_pipeline import run_data_exposition

if __name__ == "__main__":

    logger.info("-:-  STEP 1 - Run Data preparation pipeline ---------------------:-")
    data_preparation_output = run_data_prep(LIST_DATASRC)
    logger.info(data_preparation_output)

    logger.info("-:-  STEP 2 - Run Data transformation pipeline -------------------:-")
    data_transformation_output = run_data_transformation(data_preparation_output)
    logger.info(data_transformation_output)

    logger.info("-:-  STEP 3 - Run Data exposition pipeline ------------------------:-")
    data_exposition_output = run_data_exposition(data_transformation_output)

    logger.info("-:---------------Result--------------------------------------------:-")
    logger.info(data_exposition_output)


