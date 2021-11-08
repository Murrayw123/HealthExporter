from enum import Enum

from dateutil import parser
from influxdb_client import Point


class CSVPositions(Enum):
    TIMESTAMP = 1
    LIFT = 2
    WEIGHT = 3
    REPS = 4
    AREA = 9
    TITLE = 10


def add_set_to_point(current_point, previous_point, previous_row, current_row):
    if current_row[CSVPositions.LIFT.value] == previous_row[CSVPositions.LIFT.value]:
        previous_set_count = previous_point._tags.get("Set")
        current_point.tag("Set", previous_set_count + 1)
    else:
        current_point.tag("Set", 1)

    return current_point


class RepcountParser:
    def __init__(self, db_writer):
        self.__db_writer = db_writer

    def parse_rows(self, rep_list):
        points = []

        for count, row in enumerate(rep_list):
            timestamp = row[CSVPositions.TIMESTAMP.value]
            lift = row[CSVPositions.LIFT.value]
            weight = float(row[CSVPositions.WEIGHT.value])
            reps = int(row[CSVPositions.REPS.value])
            area = row[CSVPositions.AREA.value]
            title = row[CSVPositions.TITLE.value]

            time = parser.parse(timestamp)

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

            points.append(point)

        return self.__write_points(points)

    def __write_points(self, points):
        self.__db_writer(points)
