import sys
from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTranformationConfig:
    preprocessor_obj_file_path=os.path.join('artifact','preprocessor.pkl')

class DataTranformation:
    def __init__(self):
        self.Data_Tranformation_Config=DataTranformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_columns= ['writing_score','reading_score']

            cat_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch","test_preparation_course"
                ]
            
            num_pipeline=Pipeline(
                steps=[
                    ('Imputer',SimpleImputer(strategy="median")),
                    ('scaler',StandardScaler(with_mean=False))

                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]

            )

            logging.info(f'Categorical Columns: {cat_columns}')
            logging.info(f'Numerical coumns :{numerical_columns}')

            preprocessor=ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,cat_columns)
                ]
            )

            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("The train and test reading completed")
            logging.info("Obtaining preprocessing object")

            preproccessing_obj=self.get_data_transformer_obj()

            target_column_name="math_score"
            numerical_columns=['writing_score','reading_score']


            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
               f'Applying preprocessing object on training dataframe and testing dataframe')
            input_feature_train_arr=preproccessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preproccessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[
            input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr=np.c_[
            input_feature_test_arr,np.array(target_feature_test_df)
            ]
            logging.info(f'Saved preprocessing object.')

            save_object(

                file_path=self.Data_Tranformation_Config.preprocessor_obj_file_path,
                obj=preproccessing_obj

            )

            return(
                train_arr,
                test_arr,
                self.Data_Tranformation_Config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
    
        




