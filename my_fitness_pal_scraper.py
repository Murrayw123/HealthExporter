import datetime

import myfitnesspal
from influxdb_client import Point


class MyFitnessPalParser:
    def __init__(self, db_writer):
        self.__db_writer = db_writer
        self.__client = myfitnesspal.Client(
            "***REMOVED***", password="***REMOVED***"
        )

    def get_daily_summary(self):
        today = datetime.date.today()
        today_with_hours = today + datetime.timedelta(hours=11, minutes=59)

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
