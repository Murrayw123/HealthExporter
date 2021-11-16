import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from dynaconf import settings

from database import Database


def create_parsers(db_write_fn):
    return [p(db_writer=db_write_fn) for p in settings.PARSERS]


class TaskRunner(object):
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
