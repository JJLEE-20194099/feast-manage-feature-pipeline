import os
from dotenv import load_dotenv
import traceback
import time
import pandas as pd
from sqlalchemy import create_engine

load_dotenv(override=True)
import boto3

class PostgresqlDB():
    __connection_str : str
    __client : None
    __database : None
    __collection : None

    def __init__(self, db_config: str = None, connection_str:str = os.getenv('POSTGRES_SERVER_PATH'), database:str = os.getenv('POSTGRES_DATABASE')):

        self.__database = database
        self.__connection_str = f'postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER_PATH')}/{self.__database}'
        self.__client = create_engine(self.__connection_str)


    def write_file_by_df(self, df, file_name):
        df.to_sql(file_name, self.__client, if_exists='append', index=False)
        return 1

