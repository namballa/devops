from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/singhera/Downloads/bahrain-limos-647e3e538a6b.json"

client = bigquery.Client()

# Perform a query.
# QUERY = (
#     'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
#     'WHERE state = "TX" '
#     'LIMIT 100')


QUERY = (
    'SELECT * FROM `bahrain-limos.twitterdataset.twitter` '
    'WHERE id = "1467810369" '
    'LIMIT 100')

query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.target)
    print(row.id)
    print(row.date)
    print(row.flag)
    print(row.user)
    print(row.text)
   
    
    

    