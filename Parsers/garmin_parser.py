from datetime import date, datetime

from garminconnect import Garmin
from influxdb_client import Point

from Parsers.parser_interface import Parser
from dynaconf import settings


class GarminConnectParser(Parser):
    def __init__(self, db_writer):
        super().__init__(db_writer)
        try:
            self.__client = Garmin(
                settings.GARMIN_CONNECT_EMAIL, settings.GARMIN_CONNECT_PASSWORD
            )
            self.__client.login()
        except Exception as e:
            print("Garmin Connect Error", e)

    def parse(self):
        today = date.today()

        today_with_hours = datetime(today.year, today.month, today.day, 11, 59)

        steps = self.__client.get_steps_data(date.today().isoformat())
        total_steps = sum(step["steps"] for step in steps)
        daily_stats = self.__client.get_stats(date.today().isoformat())
        calories = daily_stats['totalKilocalories']
        point = (
            Point("Daily Energy")
            .field("Steps", total_steps)
            .field("Calories Burned", calories)
            .time(
                time=today_with_hours,
            )
        )
        self._db_writer(point)
