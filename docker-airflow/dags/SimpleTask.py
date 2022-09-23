from airflow import DAG
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import numpy as np
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}


def simpleNumpyToGCS(csv_name: str, folder_name: str,
                   bucket_name="hari-airflow", **kwargs):
    hook = GoogleCloudStorageHook()
    
    data = {'col1': [1, 2], 'col2': [3, 4]}

    df = pd.DataFrame(data=data)
        
    df.to_csv('example1.csv', index=False)

    hook.upload(bucket_name, 
                object='{}/{}.csv'.format(folder_name, csv_name), 
                filename='example1.csv', 
                mime_type='text/csv')


dag = DAG('SendCSVDag',
          default_args=default_args,
          catchup=False)

with dag:

    simpleNumpyToGCS_task = PythonOperator(
        task_id='simpleNumpyToGCS',
        python_callable=simpleNumpyToGCS,
        provide_context=True,
        op_kwargs={'csv_name': 'example_airflow', 'folder_name': 'singhera'},
    )

    simpleNumpyToGCS_task