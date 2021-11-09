from database import Database
from my_fitness_pal_scraper import MyFitnessPalParser
from repcount_parser import RepcountParser


class TaskRunner:
    def __init__(self):
        database = Database()
        write_fn = database.write
        self.__repcount_parser = RepcountParser(write_fn)
        self.__mfp_parser = MyFitnessPalParser(write_fn)

    def run_task(self):
        self.__repcount_parser.parse_csv()
        self.__mfp_parser.get_daily_summary()


if __name__ == '__main__':
    tr = TaskRunner()
    tr.run_task()
