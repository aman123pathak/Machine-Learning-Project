import os
import sys
import dill
import pandas as pd
import numpy as np
from pathlib import Path
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
            
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(x_train, y_train, x_test, y_test, models, param):
    try:
        report = {}
        for model_name, model in models.items():
            para=param[model_name]
            
            gs = GridSearchCV(estimator=model,param_grid=para,cv=3,scoring="r2",n_jobs=-1)
            gs.fit(x_train, y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)
            
            #model.fit(x_train, y_train)        #Train model
            
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[model_name] = test_model_score
            
        return report
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)