"""Added 2026-03 after the stale-FX incident: the EUR rate went a week out of
date and EMEA was reported 12% low. This suite watches the rate table and the
conversion arithmetic."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from revenue import transform


def rec(amount, currency):
    return {"region_code": "na", "currency": currency,
            "amount": amount, "order_id": "X"}


class RateTable(unittest.TestCase):
    def test_usd_is_identity(self):
        self.assertEqual(transform.FX_TO_USD["USD"], 1.0)

    def test_every_rate_positive(self):
        for cur, rate in transform.FX_TO_USD.items():
            self.assertGreater(rate, 0, cur)

    def test_expected_currencies_present(self):
        self.assertEqual(set(transform.FX_TO_USD), {"USD", "EUR", "JPY"})

    def test_eur_rate_in_plausible_band(self):
        self.assertTrue(0.9 <= transform.FX_TO_USD["EUR"] <= 1.3)

    def test_jpy_rate_in_plausible_band(self):
        self.assertTrue(0.005 <= transform.FX_TO_USD["JPY"] <= 0.010)


class Conversion(unittest.TestCase):
    def test_eur_regression_march_incident(self):
        # 1000 EUR must not come back as the 12%-low 959.20 we shipped in March
        self.assertAlmostEqual(transform.to_usd(rec(1000.0, "EUR"))["amount_usd"],
                               1090.0, places=6)

    def test_jpy_conversion(self):
        self.assertAlmostEqual(transform.to_usd(rec(1000.0, "JPY"))["amount_usd"],
                               6.7, places=6)

    def test_zero_amount(self):
        self.assertEqual(transform.to_usd(rec(0.0, "EUR"))["amount_usd"], 0.0)

    def test_negative_amount_refund(self):
        self.assertAlmostEqual(transform.to_usd(rec(-100.0, "EUR"))["amount_usd"],
                               -109.0, places=6)

    def test_unpriceable_currency_returns_none(self):
        self.assertIsNone(transform.to_usd(rec(100.0, "GBP")))

    def test_conversion_is_linear(self):
        a = transform.to_usd(rec(1.0, "EUR"))["amount_usd"]
        b = transform.to_usd(rec(1000.0, "EUR"))["amount_usd"]
        self.assertAlmostEqual(b, a * 1000, places=6)


if __name__ == "__main__":
    unittest.main()
