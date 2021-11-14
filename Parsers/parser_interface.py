import abc


class Parser(metaclass=abc.ABCMeta):
    def __init__(self, db_writer):
        self.__db_writer = db_writer

    @abc.abstractmethod
    def parse(cls):
        pass
