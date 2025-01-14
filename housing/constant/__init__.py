import os 
from datetime import datetime
ROOT_DIR=os.getcwd()
#config.yaml code
CONFIG_DIR='config'
CONFIG_FILE_NAME='config.yaml'
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)
#current time stamp
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

#training pipeline related variable

TRAINING_PIPELINE_CONFIG_KEY='training_pipeline_config'
TRAINING_PIPELINE_ARTIFACT_DIR='artifact_dir'
TRAINING_PIPELINE_NAME_KEY='pipeline_name'