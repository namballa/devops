import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/singhera/Downloads/bahrain-limos-647e3e538a6b.json"
#from google.cloud import bigquery_datatransfer_v1
import google.protobuf.json_format
from google.cloud import bigquery



from google.cloud import bigquery_datatransfer

client = bigquery_datatransfer.DataTransferServiceClient()

# TODO: Update to your project ID.
project_id = "bahrain-limos"

# Get the full path to your project.
parent = client.common_project_path(project_id)

print("Supported Data Sources:")

# Iterate over all possible data sources.
for data_source in client.list_data_sources(parent=parent):
   # print("{}:".format(data_source))
    print("{}:".format(data_source.display_name))
    print("\tID: {}".format(data_source.data_source_id))
    print("\tFull path: {}".format(data_source.name))
    print("\tDescription: {}".format(data_source.description))