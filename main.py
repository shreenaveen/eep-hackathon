# Copyright 2021 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START eventarc_gcs_server]
import os

from flask import Flask, request
import json
from google.cloud import bigquery

app = Flask(__name__)


# [END eventarc_gcs_server]


# [START eventarc_gcs_handler]
@app.route('/', methods=['POST'])
def index():
    # Gets the Payload data from the Audit Log
    content = request.json
    try:
        print(content)
        ds = content['resource']['labels']['dataset_id']
        proj = content['resource']['labels']['project_id']
        tbl = content['protoPayload']['resourceName']
        rows = int(content['protoPayload']['metadata']['tableDataChange']['insertedRowsCount'])
        if ds == 'team4_cloud_run' and tbl.endswith('tables/DemiseRequests') and rows > 0:
            query = update_dr()
            return "Demise request updated with host attributes", 200
    except:
        # if these fields are not in the JSON, ignore
        pass
    return "ok", 200


# [END eventarc_gcs_handler]

def update_dr():
    client = bigquery.Client()
    query = """
UPDATE
  team4_cloud_run.DemiseRequests DR
SET
  DR.MacAddress=Sccm.MacAddress,
  DR.HardwareHash=Sccm.HardwareHash,
  DR.CertifiedToRemove = 'true'
FROM
  team4_cloud_run.SCCM_SystemData Sccm
WHERE
  DR.hostname = Sccm.hostname;
INSERT INTO team4_cloud_run.forescout (id, hostname, macaddress, quarantine)
SELECT id, hostname, macaddress, 'true' FROM team4_cloud_run.DemiseRequests;
    """
    client.query(query)
    return query


# [START eventarc_gcs_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END eventarc_gcs_server]
