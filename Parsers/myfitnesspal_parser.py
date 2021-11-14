import datetime

import myfitnesspal
from influxdb_client import Point
from dynaconf import settings

from Parsers.parser_interface import Parser


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

        if day.complete:
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

