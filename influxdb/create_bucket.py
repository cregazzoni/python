import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# DB CONNECTION Parameters
influxdb_url = 'http://localhost:8086'
influxdb_token = os.environ["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
influxdb_bucket = "my_new_bucket"
influxdb_org_id = "3bcb4f6d9fed460c"

# Declare InnoDB client
my_client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org_id)

# Check if the bucket exists, if not create it
try:
    influxdb_buckets_api = my_client.buckets_api()
    bucket_objects = influxdb_buckets_api.find_buckets()

    new_bucket = influxdb_client.domain.bucket.Bucket(name=influxdb_bucket, retention_rules=[], org_id=influxdb_org_id)
    influxdb_buckets_api.create_bucket(new_bucket)
except:
    # Ignore the error if the bucket already exists
    pass

