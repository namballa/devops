from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import ClientSecretCredential, DefaultAzureCredential
import pandas as pd 
import json
from azure.storage.blob import BlobServiceClient

import os
# URL = "https://msdocs-account-cosmos-13976262.documents.azure.com:443"
# KEY = "q4raJXFtSoynx8kf1xaG8614sRieDASoh4O9VS574Tcy74WVpxyP6rwNZDwD9JdqeTEAY44tKMLNEFJOCS6vuQ=="
URL = os.environ['ACCOUNT_URI']
KEY = os.environ['ACCOUNT_KEY']

token_credential = DefaultAzureCredential()

# blob_service_client = BlobServiceClient(
#         account_url="https://csb1003200208e9eadf.blob.core.windows.net",
#         credential=KEY
#     )



connection_string = "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=csb1003200208e9eadf;AccountKey=MJbEjlASowePfDOHseBdMgEWa0fWcb3rUtnrB6pYhX+/uhOJMDfqvgrKcwGxJltYOyBd3mB0JWAv+AStIF1qgQ==;BlobEndpoint=https://csb1003200208e9eadf.blob.core.windows.net/;FileEndpoint=https://csb1003200208e9eadf.file.core.windows.net/;QueueEndpoint=https://csb1003200208e9eadf.queue.core.windows.net/;TableEndpoint=https://csb1003200208e9eadf.table.core.windows.net"

service = BlobServiceClient.from_connection_string(conn_str=connection_string)

clientStrorageBlob = service.get_container_client("hntestcontainer")
bc = clientStrorageBlob.get_blob_client(blob="s3")
data = bc.download_blob()
with open("s3.csv", "wb") as f:
   data.readinto(f)
df = pd.read_csv("s3.csv",encoding='ISO-8859–1',dtype='str')
# df = pd.read_csv('https://globaldatalab.org/assets/2019/09/SHDI%20Complete%203.0.csv',encoding='ISO-8859–1',dtype='str')

print('Blob Storage readed.',df)

client = CosmosClient(URL, credential=KEY,  consistency_level='Eventual')
DATABASE_NAME = 'testDatabase'
try:
    database = client.create_database(DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
 database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'S3'




try:
    container = database.create_container(id=CONTAINER_NAME, partition_key=PartitionKey(path="/country"))
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(CONTAINER_NAME)
except exceptions.CosmosHttpResponseError:
    raise

# for i in range(1, 10):
#     container.upsert_item({
#             'id': 'item{0}'.format(i),
#             'productName': 'Widget',
#             'productModel': 'Model {0}'.format(i)
#         }
#     )






# Reset index - creates a column called 'index'
df = df.reset_index()
# Rename that new column 'id'
# Cosmos DB needs one column named 'id'. 
df = df.rename(columns={'index':'id'})
# Convert the id column to a string - this is a document database.
df['id'] = df['id'].astype(str) 



# Write rows of a pandas DataFrame as items to the Database Container
for i in range(0,df.shape[0]):
    # create a dictionary for the selected row
    data_dict = dict(df.iloc[i,:])
    # convert the dictionary to a json object.
    data_dict = json.dumps(data_dict)
    insert_data = container.upsert_item(json.loads(data_dict))
print('Records inserted successfully.',data_dict)



dflist = []
for item in container.query_items(
        query = 'SELECT * FROM c where c.country="Afghanistan" and c.level="National"',
        enable_cross_partition_query=True):
   print(json.dumps(item, indent=True))

dflist.append(dict(item))
    
# Convert list to pandas DataFrame
df = pd.DataFrame(dflist)
df.head()