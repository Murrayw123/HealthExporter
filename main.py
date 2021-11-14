import datetime
from collections import Callable

from apscheduler.schedulers.blocking import BlockingScheduler
from influxdb_client import Point

from database import Database
from dynaconf import settings


def create_parsers(db_write_fn):
    return [p(db_writer=db_write_fn) for p in settings.PARSERS]


class TaskRunner:
    def __init__(self):
        database = Database()
        self.__parsers = create_parsers(db_write_fn=database.write)

    def run_task(self):
        print("running task at", datetime.datetime.utcnow())
        for parser in self.__parsers:
            parser.parse()


if __name__ == "__main__":
    tr = TaskRunner()
    scheduler = BlockingScheduler()
    scheduler.add_job(tr.run_task, "interval", seconds=600)
    scheduler.start()
