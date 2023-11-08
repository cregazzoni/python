import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

influxdb_url = 'http://localhost:8086'
influxdb_bucket = "my_bucket"
influxdb_org_id = "3bcb4f6d9fed460c"
influxdb_measurement = "my_measurement"
my_system = "centos01"

# Declare InnoDB client
my_client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org_id)


try:

	# how I get my_data, that's not important for this snippet
	my_data = dataJson['defaultReplicaSet']['topology'][innodb_host]['replicationLag']

	# I need to convert my_data in seconds - a data format readable by InfluxDB
	timestamp = datetime.datetime.strptime(my_data, "%H:%M:%S.%f")
	my_data_in_sec = (timestamp.hour * 3600) + (timestamp.minute * 60) + timestamp.second + timestamp.microsecond / 1e6

	write_api = my_client.write_api(write_options=SYNCHRONOUS)

	# Push my_data info to InfluxDB
	p = influxdb_client.Point(str(influxdb_measurement)).tag("system", my_system).field("my_data", int(my_data_in_sec))
	write_api.write(bucket=influxdb_bucket, org=influxdb_org_id, record=p)

	print(f"{influxdb_measurement} has been updated on InfluxDB {influxdb_url}")

except Exception as e:
	print(f"Script execution is failed - {e}")

