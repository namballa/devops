from airflow import DAG
from google.cloud import storage
from google.oauth2 import service_account
from airflow.operators.python_operator import PythonOperator
from io import BytesIO, StringIO

import pandas as pd
import numpy as np
from datetime import datetime
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3
}

def return_byte_object(bucket, path: str) -> BytesIO:
    
    blob = bucket.blob(path)
    byte_object = BytesIO()
    blob.download_to_file(byte_object)
    byte_object.seek(0)

    return byte_object


def transformFromGCS(csv_name: str, folder_name: str, project: str='trusty-charmer-276704', credentials_path: str=None,
                   bucket_name="airflowexample", **kwargs):
    logging.info("*************************************Inside of transformation function************************************")
    '''
    There is another way of using google cloud storage, it is by utiliting the google_cloud library.
    I prefer using google_cloud this way for more control.
    '''
    # setting up credential and client
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project, credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    
    #create the byte stream from the csv file
    fileobj = return_byte_object(bucket, path="airflow/example_airflow.csv")
    #load the byte stream into panda
    df = pd.read_csv(fileobj)


    #you can access the log in airflow's log
    logging.info("This is File: {}".format(df))
    
    #multiplying all number column by 5
    df[df.select_dtypes(include=['number']).columns] *= 5

    logging.info("This is after file: {}".format(df))

    #re-upload a different file into google cloud bucket
    bucket.blob('{}/{}.csv'.format(folder_name, csv_name)).upload_from_string(df.to_csv(), 'text/csv')


dag = DAG('GCPAIDag',
          default_args=default_args,
          catchup=False)

with dag:

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transformFromGCS,
        provide_context=True,
        op_kwargs={'csv_name': 'example_2_airflow', 'folder_name': 'airflow', 'credentials_path': '/usr/local/airflow/dags/gcp.json'},
    )

    transform_task