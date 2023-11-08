import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Simply way to get an organization_id from InfluxDB, using influxdb-python library 

# DB CONNECTION Parameters
influxdb_url = 'http://localhost:8086'
influxdb_token = os.environ["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
influxdb_bucket = "msc-innodb-replication-lag"

# 
authorization_token = f"Bearer {influxdb_token}"
endpoint = f"{influxdb_url}/api/v2/orgs"
headers = {
    "Authorization": authorization_token
}

# Send the GET request
response = requests.get(endpoint, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    orgs_data = response.json()

    # Extract and print the IDs of the organizations
    for org in orgs_data['orgs']:
        if org['name'] == "influxdata":
            influxdb_org_id = org['id']
            print(f"DEBUG - ORG_ID: {influxdb_org_id}")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
