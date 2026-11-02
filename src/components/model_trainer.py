import sys
import os
from pathlib import Path
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor)

from sklearn.linear_model import (
    LinearRegression,
    Lasso,
    Ridge
)
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_models

PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=(PROJECT_ROOT / "artifacts" / "model.pkl")
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
        
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("split training and test input data")
            x_train, y_train, x_test, y_test = (train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1])
            
            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error'],
                },
                "Random Forest Regressor":{
                    'n_estimators': [32,64,128]
                },
                "Linear Regression":{},
                "K-Neighbors Regressor":{
                    'n_neighbors':[5,7,9],
                },
                "XGBRegressor":{
                    'learning_rate':[.01,.05,.1],
                    'n_estimators': [32,64,128]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.01,0.1,0.5,],
                    'n_estimators': [32,64,128]
                },
                "Lasso": {
                    'alpha': [0.001, 0.01, 0.1, 1.0, 10.0],
                },
                "Ridge": {
                    'alpha': [0.001, 0.01, 0.1, 1.0, 10.0],
                }
            }
            
            model_report=evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, param=params)
            
            best_model_name = max(model_report, key=model_report.get)

            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException("No model achieved the minimum R2 score of 0.6", sys)
            
            logging.info(
                f"Best model: {best_model_name}, "
                f"R2 Score: {best_model_score}"
            )
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            predicted=best_model.predict(x_test)
            r2_square = r2_score(y_test, predicted)
            logging.info(
                f"Final model R2 score: {r2_square}"
            )
            return r2_square
        
        except Exception as e:
            raise CustomException(e, sys)