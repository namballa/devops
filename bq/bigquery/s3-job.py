import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/singhera/Downloads/bahrain-limos-647e3e538a6b.json"
from google.cloud import bigquery_datatransfer_v1
import google.protobuf.json_format
from google.cloud import bigquery



def create_scheduled_query(override_values={}):
    # [START bigquerydatatransfer_create_scheduled_query]
    # [START bigquerydatatransfer_create_scheduled_query_with_service_account]
    from google.cloud import bigquery_datatransfer
    from google.cloud import bigquery

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()
    # print(transfer_client.DEFAULT_ENDPOINT)


    schema = [
    bigquery.SchemaField("target", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("date", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("flag", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("user", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("user", "INTEGER", mode="REQUIRED"),
            ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )


    # The project where the query job runs is the same as the project
    # containing the destination dataset.
    project_id = "bahrain-limos"
    dataset_id = "twitter"

    # This service account will be used to execute the scheduled queries. Omit
    # this request parameter to run the query as the user with the credentials
    # associated with this client.
    service_account_name = "975536061309@cloudservices.gserviceaccount.com"
    # [END bigquerydatatransfer_create_scheduled_query_with_service_account]
    # [END bigquerydatatransfer_create_scheduled_query]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("bahrain-limos", project_id)
    dataset_id = override_values.get("twitter", dataset_id)
    service_account_name = override_values.get(
        "service_account_name", service_account_name
    )
    # [START bigquerydatatransfer_create_scheduled_query]
    # [START bigquerydatatransfer_create_scheduled_query_with_service_account]

    # Use standard SQL syntax for the query.


    parent = transfer_client.common_project_path(project_id)
    transfer_config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id=dataset_id,
        display_name="amazon s3 job from python with hari final",
        data_source_id="amazon_s3",
        params={
        "destination_table_name_template":"twitter_01",
        "data_path":"s3://ebh/csv/training.1600000.processed.noemoticon.csv",
        "access_key_id": "AKIA4HVDLNURI7N3FWHV",
        "secret_access_key":"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",
        "file_format": "CSV"
    },
        schedule="every 24 hours",
    )

    transfer_config = transfer_client.create_transfer_config(
        bigquery_datatransfer.CreateTransferConfigRequest(
            parent=parent,
            transfer_config=transfer_config
        )
    )

    print("Created Amazon Transfer '{}'".format(transfer_config.name))
    # [END bigquerydatatransfer_create_scheduled_query_with_service_account]
    # [END bigquerydatatransfer_create_scheduled_query]
    # Return the config name for testing purposes, so that it can be deleted.
    return transfer_config


create_scheduled_query()