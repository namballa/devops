import pandas as pd 
import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
import os
print('Imported packages successfully.')

# Initialize the Cosmos client

config = {
    "endpoint": os.environ['ACCOUNT_URI']
    "primarykey": os.environ['ACCOUNT_KEY']
}

# Create the cosmos client
client = cosmos_client.CosmosClient(url_connection=config["endpoint"], auth={"masterKey":config["primarykey"]}
)

database_name = 'HDIdatabase'
try:
    database = client.CreateDatabase({'id': database_name})
except errors.HTTPFailure:
    database = client.ReadDatabase("dbs/" + database_name)

    database_link = 'dbs/' + 'HDIdatabase'
container_definition = {'id': 'HDIcontainer',
                        'partitionKey':
                                    {
                                        'paths': ['/country'],
                                        'kind': documents.PartitionKind.Hash
                                    }
                        }
try:
    container = client.CreateContainer(database_link=database_link, 
                                        collection=container_definition, 
                                        options={'offerThroughput': 400})
except errors.HTTPFailure as e:
    if e.status_code == http_constants.StatusCodes.CONFLICT:
        container = client.ReadContainer("dbs/" + database['id'] + "/colls/" + container_definition['id'])
    else:
        raise e

df = pd.read_csv('https://globaldatalab.org/assets/2019/09/SHDI%20Complete%203.0.csv',encoding='ISO-8859–1',dtype='str')
# Reset index - creates a column called 'index'
df = df.reset_index()
# Rename that new column 'id'
# Cosmos DB needs one column named 'id'. 
df = df.rename(columns={'index':'id'})
# Convert the id column to a string - this is a document database.
df['id'] = df['id'].astype(str) 


collection_link = database_link + '/colls/' + 'HDIcontainer'

# Write rows of a pandas DataFrame as items to the Database Container
for i in range(0,df.shape[0]):
    # create a dictionary for the selected row
    data_dict = dict(df.iloc[i,:])
    # convert the dictionary to a json object.
    data_dict = json.dumps(data_dict)
    insert_data = client.UpsertItem(collection_link,json.loads(data_dict)
    )
print('Records inserted successfully.')

dflist = []
# Connection link
collection_link = database_link + '/colls/' + 'HDIcontainer'
# Write out query
query = 'SELECT * FROM c where c.country="Afghanistan" and c.level="National"'

# For-loop to retrieve individual json records from Cosmos DB 
# that satisfy our query
for item in client.QueryItems(collection_link,
                              query,
                              {'enableCrossPartitionQuery': True}
                              ):
    # Append each item as a dictionary to list
    dflist.append(dict(item))
    
# Convert list to pandas DataFrame
df = pd.DataFrame(dflist)
df.head()