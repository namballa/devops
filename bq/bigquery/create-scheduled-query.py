from google.cloud import bigquery
import google.protobuf.json_format
from google.cloud import bigquery_datatransfer_v1
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/singhera/Downloads/bahrain-limos-647e3e538a6b.json"


def create_scheduled_query(override_values={}):
    # [START bigquerydatatransfer_create_scheduled_query]
    # [START bigquerydatatransfer_create_scheduled_query_with_service_account]
    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    # The project where the query job runs is the same as the project
    # containing the destination dataset.
    project_id = "bahrain-limos"
    dataset_id = "bqdataset10"

    # This service account will be used to execute the scheduled queries. Omit
    # this request parameter to run the query as the user with the credentials
    # associated with this client.
    service_account_name = "bq-python-336@bahrain-limos.iam.gserviceaccount.com"
    # [END bigquerydatatransfer_create_scheduled_query_with_service_account]
    # [END bigquerydatatransfer_create_scheduled_query]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("bahrain-limos", project_id)
    dataset_id = override_values.get("bqdataset10", dataset_id)
    service_account_name = override_values.get(
        "service_account_name", service_account_name
    )
    # [START bigquerydatatransfer_create_scheduled_query]
    # [START bigquerydatatransfer_create_scheduled_query_with_service_account]

    # Use standard SQL syntax for the query.

    query_string = """
    SELECT
      CURRENT_TIMESTAMP() as current_time,
      @run_time as intended_run_time,
      @run_date as intended_run_date,
      17 as some_integer
    """

    parent = transfer_client.common_project_path(project_id)

    transfer_config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id=dataset_id,
        display_name="Your Scheduled Query Name",
        data_source_id="scheduled_query",
        params={
            "query": query_string,
            "destination_table_name_template": "your_table_{run_date}",
            "write_disposition": "WRITE_TRUNCATE",
            "partitioning_field": "",
        },
        schedule="every 24 hours",
    )

    transfer_config = transfer_client.create_transfer_config(
        bigquery_datatransfer.CreateTransferConfigRequest(
            parent=parent,
            transfer_config=transfer_config,
            service_account_name=service_account_name,
        )
    )

    print("Created scheduled query '{}'".format(transfer_config.name))
    # [END bigquerydatatransfer_create_scheduled_query_with_service_account]
    # [END bigquerydatatransfer_create_scheduled_query]
    # Return the config name for testing purposes, so that it can be deleted.
    return transfer_config


create_scheduled_query()
