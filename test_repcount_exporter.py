import csv
import unittest
from unittest.mock import Mock

from repcount_parser import RepcountParser


class TestRepcountExporter(unittest.TestCase):
    def setUp(self) -> None:
        self.__writer_fn = Mock()
        self.__repcount_parser = RepcountParser(self.__writer_fn)

    def test_csv_parse(self):
        with open("repcount_csv_export.csv") as repcount_export:
            reader = csv.reader(repcount_export, delimiter=",")
            next(reader)

            self.__repcount_parser.parse_rows(list(reader))
            res = self.__writer_fn.call_args

            row = res.args[0][0]
            self.assertEqual(row.to_line_protocol(), 'High\ Bar\ Squat,unit=kg,workout\ area=Legs,workout\ name=Friday\ workout Lift="High Bar Squat",Reps=1i,Set=1i,Weight=100 1636135440000000000')
