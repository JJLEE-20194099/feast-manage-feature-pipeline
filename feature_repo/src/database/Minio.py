import os
from dotenv import load_dotenv
import traceback
import time
from minio import Minio
from minio.error import S3Error
from io import StringIO
import pandas as pd

load_dotenv(override=True)
import boto3

class MinioDb():
    __connection_str : str
    __client : None
    __database : None
    __collection : None

    def __init__(self, db_config: str = None, connection_str:str = os.getenv('MINIO_SERVER_PATH'), database:str = None):

        self.connection_str = connection_str
        self.__client = Minio(self.connection_str,
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_ACCESS_KEY'),
            secure=False
        )
        self.s3 = boto3.resource('s3',
        endpoint_url=f'http://{connection_str}/',
        aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('MINIO_SECRET_ACCESS_KEY'),
        aws_session_token=None,
        verify=False)

        self.database = database


    def create_bucket(self, bucket_name):
        found = self.__client.bucket_exists(bucket_name)
        if not found:
            self.__client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")

    def get_file(self, bucket_name, dest_file_name, file_format='csv', delete=False):
        obj = self.s3.Object(bucket_name=bucket_name, key=dest_file_name).get()
        data_string = obj['Body'].read().decode("utf-8")
        if delete:
            self.s3.Object(bucket_name=bucket_name, key=dest_file_name).delete()
        if file_format == 'csv':
            df = pd.read_csv(StringIO(data_string))
        return df

    def upload_file(self, bucket_name, source_path, dest_file_name):
        start_time = time.perf_counter()
        print ("update data start -->>>>>>>>")

        self.create_bucket(bucket_name)
        self.__client.fput_object(
            bucket_name, dest_file_name, source_path,
        )

        print(
            source_path, "successfully uploaded as object",
            dest_file_name, "to bucket", bucket_name,
        )

        stop_time = time.perf_counter()
        print (f"updated data sucessfully in {stop_time-start_time} seconds -->>>>>>>>")

