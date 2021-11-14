from datetime import date

from garminconnect import Garmin

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
        steps = self.__client.get_steps_data(date.today().isoformat())


if __name__ == "__main__":
    def thing(point):
        print(point)

    parser = GarminConnectParser(thing)
    parser.parse()
    print ('hello world 1')




