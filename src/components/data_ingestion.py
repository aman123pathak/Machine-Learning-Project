import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass
class DataIngestionConfig:
    train_data_path: str=PROJECT_ROOT / "artifacts" / "train.csv"
    test_data_path: str=PROJECT_ROOT / "artifacts" / "test.csv"
    raw_data_path: str=PROJECT_ROOT / "artifacts" / "data.csv"
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()  
        
    def initiate_data_ingestion(self): 
        logging.info("Entered the data ingestion method or component")
        try:
            # Read original dataset
            data_path = PROJECT_ROOT / "notebook" / "data" / "stud.csv"
            
            df=pd.read_csv(data_path)
            logging.info('Read the dataset as dataframe')
            
            artifacts_dir = PROJECT_ROOT / "artifacts" 
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info(f"Training dataset shape: {train_set.shape}")
            logging.info(f"Testing dataset shape: {test_set.shape}")
            logging.info("Ingestion of data is completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error("Error occurred during data ingestion")
            raise CustomException(e, sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_transformation=DataTransformation()
    train_arr, test_arr, _=data_transformation.initiate_data_transformation(train_data, test_data)
    
    Modeltrainer = ModelTrainer()
    print(Modeltrainer.initiate_model_trainer(train_arr, test_arr))