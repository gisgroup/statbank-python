from statbank import time, error

import unittest
from datetime import datetime


class TestTime(unittest.TestCase):

    def test_year(self):
        timestring = "2015"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 1, 1))

    def test_year_interval(self):
        timestring = "2000:2015"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2000, 1, 1))

    def test_season(self):
        timestring = "2000/2015"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2000, 1, 1))

    def test_halfyear_1(self):
        timestring = "2015H1"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 1, 1))

    def test_halfyear_2(self):
        timestring = "2015H2"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 7, 1))

    def test_halfyear_invalid(self):
        timestring = "2015H3"
        with self.assertRaises(error.TimeError):
            time.parse(timestring)

    def test_quarter(self):
        timestring = "2015K4"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 10, 1))

    def test_quarter_english(self):
        timestring = "2015Q4"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 10, 1))

    def test_quarter_invalid(self):
        timestring = "2015K5"
        with self.assertRaises(error.TimeError):
            time.parse(timestring)

    def test_month_1(self):
        timestring = "2015M1"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 1, 1))

    def test_month_12(self):
        timestring = "2015M12"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 12, 1))

    def test_month_zeropad(self):
        timestring = "2015M01"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 1, 1))

    def test_month_invalid(self):
        timestring = "2015M713"
        with self.assertRaises(error.TimeError):
            time.parse(timestring)

    def test_week_interval_1(self):
        timestring = "2015U1-13"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2014, 12, 29))

    def test_week_interval_1_zeropad(self):
        timestring = "2015U01-13"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2014, 12, 29))

    def test_week_interval_2(self):
        timestring = "2015U31-48"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 7, 27))

    def test_week_interval_invalid(self):
        timestring = "2015U0-42"
        with self.assertRaises(error.TimeError):
            time.parse(timestring)

    def test_day_2(self):
        timestring = "2015M1D2"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 1, 2))

    def test_day_zeropad(self):
        timestring = "2015M01D02"
        parsed = time.parse(timestring)
        self.assertEqual(parsed, datetime(2015, 1, 2))

if __name__ == '__main__':
    unittest.main()
