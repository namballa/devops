from airflow import DAG
from google.cloud import storage
from google.oauth2 import service_account
from airflow.operators.python_operator import PythonOperator
from io import BytesIO, StringIO

import pandas as pd
import numpy as np
from datetime import datetime
import logging

from airflow.contrib.sensors import gcs_sensor


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}


def delete_file(bucket_name, blob_name, project, credentials_path: str=None, **kwargs):
    """Deletes a blob from the bucket."""

    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project, credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    logging.info("Blob {} deleted.".format(blob_name))



dag = DAG('DeleteBucketDag',
          default_args=default_args,
          catchup=False)

with dag:
    delete_task = PythonOperator(
        task_id='delete_file',
        python_callable=delete_file,
        provide_context=True,
        op_kwargs={'bucket_name': 'airflowexample', 'blob_name': 'airflow/example_airflow.csv', 'project': 'trusty-charmer-276704', 'credentials_path': '/usr/local/airflow/dags/gcp.json'},
    )

    checkFileSensor = gcs_sensor.GoogleCloudStorageObjectSensor(
        task_id='gcs_sensor_example1',
        bucket='airflowexample',
        object='airflow/example_airflow.csv',
        google_cloud_conn_id='google_cloud_default',
        timeout=60, # timeout in 1 min
        poke_interval=20, # checking file every 20 seconds
        soft_fail=True #skip tasks if it is False
    )

    checkFileSensor >> delete_task