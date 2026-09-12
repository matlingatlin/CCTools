import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from revenue import extract

CSV = """order_id,region,currency,amount
A-1,North America,USD,1234.50
A-2,EMEA,EUR,"2.000,25"
A-3,APAC,JPY,500000
"""


class ToMinorUnits(unittest.TestCase):
    def test_dot_decimal(self):
        self.assertEqual(extract._to_minor_units("1234.50"), 123450)

    def test_comma_decimal(self):
        self.assertEqual(extract._to_minor_units("2.000,25"), 200025)

    def test_integer(self):
        self.assertEqual(extract._to_minor_units("500000"), 50000000)

    def test_returns_int(self):
        self.assertIsInstance(extract._to_minor_units("9.99"), int)


class ParseRows(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(CSV)

    def tearDown(self):
        os.unlink(self.path)

    def test_row_count(self):
        self.assertEqual(len(extract.parse_rows(self.path)), 3)

    def test_region_codes(self):
        codes = [r["region_code"] for r in extract.parse_rows(self.path)]
        self.assertEqual(codes, ["na", "emea", "apac"])

    def test_currency_uppercased(self):
        self.assertEqual(extract.parse_rows(self.path)[1]["currency"], "EUR")

    def test_amounts_are_minor_units(self):
        amounts = [r["amount"] for r in extract.parse_rows(self.path)]
        self.assertEqual(amounts, [123450, 200025, 50000000])


if __name__ == "__main__":
    unittest.main()
