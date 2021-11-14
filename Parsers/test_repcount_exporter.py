import csv
import unittest
from unittest.mock import Mock

from Parsers.repcount_parser import RepcountParser


class TestRepcountExporter(unittest.TestCase):
    def setUp(self) -> None:
        self.__writer_fn = Mock()
        self.__repcount_parser = RepcountParser(self.__writer_fn)

    def test_csv_parse(self):
        with open("../TestData/repcount_csv_export.csv") as repcount_export:
            reader = csv.reader(repcount_export, delimiter=",")
            next(reader)

            self.__repcount_parser._parse_rows(list(reader))
            res = self.__writer_fn.call_args

            row = res.args[0][0]

            self.assertEqual(
                row.to_line_protocol(),
                """Straight\ Leg\ Deadlifts,Set=1,unit=kg,workout\ area=Legs,workout\ name=Saturday Lift="Straight Leg Deadlifts",RPE=6i,Reps=8i,Weight=100 1636770900000000000"""
            )
