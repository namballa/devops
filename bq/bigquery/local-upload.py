

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import csv
def merge_csv_fields (filename,output):

 with open(filename) as f:
    reader = csv.reader(f)
    with open(output, 'w') as g:
        writer = csv.writer(g)
        for row in reader:
            new_row = [' '.join([row[0], row[1]])] + row[2:]
            writer.writerow(new_row)

def load_table_file(file_path: str, result_file,table_id: str) -> "bigquery.Table":

    # [START bigquery_load_from_file]
    from google.cloud import bigquery
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bahrain-limos-bc2d0ef1ed06.json"

    # Construct a BigQuery client object.
    merge_csv_fields(file_path,result_file)
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    with open(result_file, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
    # [END bigquery_load_from_file]
    return table

load_table_file("us-states-by-date.csv","success.csv","bahrain-limos.twitter.hina")
