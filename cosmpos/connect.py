from azure.cosmos import CosmosClient
from azure.identity import ClientSecretCredential, DefaultAzureCredential

import os
URL =  
KEY = os.environ['ACCOUNT_KEY']
client = CosmosClient(URL, credential=KEY, consistency_level='EVENTUAL')
DATABASE_NAME = 'testDatabase from api python'
try:
    database = client.create_database(DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# # Using ClientSecretCredential
# # aad_credentials = ClientSecretCredential(
# #     tenant_id=tenant_id,
# #     client_id=client_id,
# #     client_secret=client_secret)

# # # Using DefaultAzureCredential (recommended)
# # aad_credentials = DefaultAzureCredential()

# # client = CosmosClient(url, aad_credentials)

# from azure.cosmos import CosmosClient
# from azure.identity import ClientSecretCredential, DefaultAzureCredential

# import os
# url = "https://msdocs-account-cosmos-13976262.documents.azure.com:443/"
# tenant_id = "873edf61-f432-4587-81cb-46a7eedee8ab"
# client_id = "1cde67c1-b1cf-42fb-8f23-b8a796e78238"
# client_secret = "ad4f5b27-8d6b-42b2-802b-b65efb49ea6a"

# # Using ClientSecretCredential
# aad_credentials = ClientSecretCredential(
#     tenant_id=tenant_id,
#     client_id=client_id,
#     client_secret=client_secret)

# # Using DefaultAzureCredential (recommended)
# aad_credentials = DefaultAzureCredential()

# client = CosmosClient(url, aad_credentials)
