import datetime

import myfitnesspal
import pytz
from influxdb_client import Point
from dynaconf import settings

from Parsers.parser_interface import Parser


def is_end_of_day(today):
    tz = pytz.timezone("Australia/Perth")

    perth_now = datetime.datetime.now()
    tz.localize(perth_now)

    end_of_day = datetime.datetime(
        year=today.year, month=today.month, day=today.day, hour=23, minute=30
    )
    tz.localize(end_of_day)

    return perth_now > end_of_day


class MyFitnessPalParser(Parser):
    def __init__(self, db_writer):
        super().__init__(db_writer)

        self.__client = myfitnesspal.Client(
            settings.MYFITNESSPAL_EMAIL, password=settings.MYFITNESSPAL_PASSWORD
        )

    def parse(self):
        today = datetime.date.today()
        today_with_hours = datetime.datetime(today.year, today.month, today.day, 11, 59)

        day = self.__client.get_date(today.year, today.month, today.day)

        if day.complete or is_end_of_day(today):
            weight = float(list(self.__client.get_measurements("Weight").items())[0][1])
            point = (
                Point("Daily Summary")
                .field("Protein", day.totals.get("protein"))
                .field("Calories", day.totals.get("calories"))
                .field("Weight", weight)
                .time(
                    time=today_with_hours,
                )
            )
            self.__db_writer(point)
