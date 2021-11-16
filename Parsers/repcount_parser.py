import csv
import re
from enum import Enum

import dropbox
import pytz
from dateutil import parser
from dropbox.exceptions import ApiError
from dynaconf import settings
from influxdb_client import Point

from Parsers.parser_interface import Parser


class CSVPositions(Enum):
    TIMESTAMP = 1
    LIFT = 2
    WEIGHT = 3
    REPS = 4
    NOTE = 5
    AREA = 9
    TITLE = 10


def add_set_to_point(current_point, previous_point, previous_row, current_row):
    if current_row[CSVPositions.LIFT.value] == previous_row[CSVPositions.LIFT.value]:
        previous_set_count = previous_point._tags.get("Set")
        current_point.tag("Set", previous_set_count + 1)
    else:
        current_point.tag("Set", 1)

    return current_point


def add_rpe_to_point(rpe, current_point):
    current_rpe = int("".join(filter(str.isdigit, rpe)))
    current_point.field("RPE", current_rpe)
    return current_point


REPCOUNT_CSV_FILE = "repcount_csv_export.csv"


class RepcountParser(Parser):
    def parse(self):
        with dropbox.Dropbox(oauth2_access_token=settings.DROP_BOX_OAUTH_TOKEN) as dbx:
            try:
                dbx.files_download_to_file(f"./{REPCOUNT_CSV_FILE}", f"/{REPCOUNT_CSV_FILE}")
                with open(f"./{REPCOUNT_CSV_FILE}") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    next(csv_reader)
                    self._parse_rows(list(csv_reader))
                dbx.files_delete_v2(f"/{REPCOUNT_CSV_FILE}")
            except ApiError as e:
                print(e)

    def _parse_rows(self, rep_list):
        points = []

        for count, row in enumerate(rep_list):
            timestamp = row[CSVPositions.TIMESTAMP.value]
            lift = row[CSVPositions.LIFT.value]
            weight = float(row[CSVPositions.WEIGHT.value])
            reps = int(row[CSVPositions.REPS.value])
            area = row[CSVPositions.AREA.value]
            title = row[CSVPositions.TITLE.value]
            note = row[CSVPositions.NOTE.value]

            time = parser.parse(timestamp)
            perth_timezone = pytz.timezone("Australia/Perth")
            time = perth_timezone.localize(time)

            point = (
                Point(lift)
                .tag("workout area", area)
                .tag("workout name", title)
                .tag("unit", "kg")
                .field("Lift", lift)
                .field("Weight", weight)
                .field("Reps", reps)
                .time(time=time)
            )

            if count == 0:
                point.tag("Set", 1)
            else:
                point = add_set_to_point(
                    current_point=point,
                    previous_point=points[count - 1],
                    current_row=row,
                    previous_row=rep_list[count - 1],
                )

            rpe = re.search("(?i)RPE: [0-9]", note)

            if rpe:
                point = add_rpe_to_point(rpe=rpe.group(0), current_point=point)

            points.append(point)
            self.__write_points(point)

        return self.__write_points(points)

    def __write_points(self, points):
        self._db_writer(points)
