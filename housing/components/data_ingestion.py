from housing.logger import logging 
from housing.exception import HousingException
from housing.entity.config_entity import DataIngestionConfig
import sys,os
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile
from six.moves import urllib
import pandas as pd 
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log has started.{'='*20}")
            self.data_ingestion_config=data_ingestion_config
            
        except Exception as e:
            raise HousingException(e,sys) from e 
    
    def download_housing_data(self)->str:
        try:
            #extraction remote url to download url
            download_url=self.data_ingestion_config.dataset_download_url
            logging.info('downloading file')

            #folder location to save file downloaded
            tgz_dowload_dir=self.data_ingestion_config.tgz_download_dir
            if os.path.exists(tgz_dowload_dir):
                os.remove(tgz_dowload_dir)
            os.makedirs(tgz_dowload_dir,exist_ok=True)
            logging.info('setting file location')

            housing_file_name=os.path.basename(download_url)
            logging.info('extracting file name from url')

            tgz_file_path=os.path.join(tgz_dowload_dir,housing_file_name)

            urllib.request.urlretrieve(download_url,tgz_file_path)
            logging.info('file has been downloaded')

            return tgz_file_path

        except Exception as e:
            raise HousingException(e,sys)

    def extract_tgz_file(self,tgz_file_path):
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            
            logging.info(f'extracting tgz file path into raw data_dir')

            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info('extracting completed')

            logging.info(f'extracting tgz file path into raw')
        except Exception as e:
            raise HousingException(e,sys) from e


    def split_data_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            file_name=os.listdir(raw_data_dir)[0]

            housing_file_path=os.path.join(raw_data_dir,file_name)

            housing_data_frame=pd.read_csv(housing_file_path)

            housing_data_frame['income_cat']=pd.cut(
                housing_data_frame['median_income'],
                bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
                labels=[1,2,3,4,5]
            )
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact


        except Exception as e:
            raise HousingException(e,sys) from e
    
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path=self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_train_test()
        except Exception as e:
            raise HousingException(e,sys)
        
    


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")