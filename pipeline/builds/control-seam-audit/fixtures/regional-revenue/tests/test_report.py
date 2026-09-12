import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from revenue import report


def row(code, total):
    return {"region_code": code, "total": total}


class Rank(unittest.TestCase):
    def test_highest_first(self):
        out = report.rank([row("na", 10.0), row("emea", 30.0), row("apac", 20.0)])
        self.assertEqual([r["region_code"] for r in out], ["emea", "apac", "na"])

    def test_single_row(self):
        self.assertEqual(len(report.rank([row("na", 1.0)])), 1)

    def test_empty(self):
        self.assertEqual(report.rank([]), [])

    def test_negative_totals_sort_last(self):
        out = report.rank([row("na", -5.0), row("emea", 1.0)])
        self.assertEqual(out[0]["region_code"], "emea")


class Render(unittest.TestCase):
    def test_names_are_displayed(self):
        text = report.render([row("na", 10.0), row("emea", 30.0)])
        self.assertIn("North America", text)
        self.assertIn("EMEA", text)

    def test_top_region_line(self):
        text = report.render([row("na", 10.0), row("emea", 30.0)])
        self.assertIn("Top region: EMEA", text)

    def test_amount_formatting(self):
        text = report.render([row("na", 1234.5)])
        self.assertIn("$1234.50", text)


if __name__ == "__main__":
    unittest.main()
