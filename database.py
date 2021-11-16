from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List
from dynaconf import settings


class Database(object):
    def __init__(self):
        client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG,
            debug=True,
        )

        self.__write_api = client.write_api(write_options=SYNCHRONOUS)

    def write(self, points: Point or List[Point]):
        self.__write_api.write(org=settings.INFLUXDB_ORG, bucket=settings.INFLUX_DB_BUCKET, record=points)
