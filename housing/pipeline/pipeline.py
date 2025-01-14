from housing.exception import HousingException
from housing.logger import logging

from housing.entity .artifact_entity import DataIngestionArtifact
from housing.entity.config_entity  import DataIngestionConfig
from housing.components .data_ingestion import DataIngestion,DataIngestionArtifact
from housing.config.configuration import Configuartion
import os,sys

class Pipeline:

    def __init__(self,config:Configuartion = Configuartion())->None:
        try:
            self.config=config
        except Exception as e:
            raise HousingException(e,sys)
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion=DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def run_pipeline(self):
        try:
            data_ingesion_artifact=self.start_data_ingestion()

        except Exception as e:
            raise HousingException(e,sys) from e

