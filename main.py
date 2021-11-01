from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision

# You can generate an API token from the "API Tokens Tab" in the UI
from influxdb_client.client.write_api import SYNCHRONOUS

token = "fYwCjtTqJk1JUAwuBbNS6NupdjnjXRgKzPnZ_68xebPMxBWq-xAXeG5chf6185KPA6VfM4JBEgN5ZvmY7zvTTg=="
org = "***REMOVED***"
bucket = "murraycwatts's Bucket"

client = InfluxDBClient(url="***REMOVED***", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

point = Point("Romanian Dead Lift") \
    .tag("type", "Deadlift") \
    .field("Weight", 75) \
    .field("Unit", "kg") \
    .field("Reps", 7) \
    .time(datetime.utcnow(), WritePrecision.NS)

write_api.write(bucket, org, point)
