from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List


class Database:
    def __init__(self):
        self.__token = "***REMOVED***"
        self.__org = "***REMOVED***"
        self.__bucket = "***REMOVED***"

        client = InfluxDBClient(
            url="***REMOVED***",
            token=self.__token,
            org=self.__org,
            debug=True,
        )

        self.__write_api = client.write_api(write_options=SYNCHRONOUS)

    def get_bucket(self):
        return self.__bucket

    def write(self, points: Point or List[Point]):
        self.__write_api.write(org=self.__org, bucket=self.__bucket, record=points)
