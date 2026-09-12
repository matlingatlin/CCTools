import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from revenue import transform


def rec(amount, currency="USD", region="na"):
    return {"region_code": region, "currency": currency,
            "amount": amount, "order_id": "X"}


class ToUsd(unittest.TestCase):
    def test_usd_unchanged(self):
        self.assertEqual(transform.to_usd(rec(100.0))["amount_usd"], 100.0)

    def test_eur_converted(self):
        self.assertAlmostEqual(
            transform.to_usd(rec(100.0, "EUR"))["amount_usd"], 109.0)

    def test_unknown_currency_is_none(self):
        self.assertIsNone(transform.to_usd(rec(100.0, "XYZ")))

    def test_original_fields_kept(self):
        out = transform.to_usd(rec(50.0, "USD", "emea"))
        self.assertEqual(out["region_code"], "emea")
        self.assertEqual(out["order_id"], "X")


class Aggregate(unittest.TestCase):
    def test_sums_within_region(self):
        rows = transform.aggregate([rec(10.0), rec(15.0)])
        self.assertEqual(rows, [{"region_code": "na", "total_usd": 25.0}])

    def test_splits_regions(self):
        rows = transform.aggregate([rec(10.0, "USD", "na"),
                                    rec(20.0, "USD", "emea")])
        totals = {r["region_code"]: r["total_usd"] for r in rows}
        self.assertEqual(totals, {"na": 10.0, "emea": 20.0})

    def test_mixed_currency_region(self):
        rows = transform.aggregate([rec(100.0, "USD"), rec(100.0, "EUR")])
        self.assertAlmostEqual(rows[0]["total_usd"], 209.0)

    def test_empty_input(self):
        self.assertEqual(transform.aggregate([]), [])


if __name__ == "__main__":
    unittest.main()
