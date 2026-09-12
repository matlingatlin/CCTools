"""Stage 1 - read the raw regional feeds and normalise them into records.

Amounts are normalised to MINOR UNITS (cents) as integers, because the feeds
disagree about decimal separators and floats were losing pennies on the EU feed.
"""
import csv


REGION_CODES = {"North America": "na", "EMEA": "emea", "APAC": "apac"}


def _to_minor_units(raw):
    """'1234.50' -> 123450. Accepts comma or dot as the decimal separator."""
    s = str(raw).strip().replace(" ", "")
    # Whichever separator comes last is the decimal one; the other groups digits.
    if s.rfind(",") > s.rfind("."):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    return int(round(float(s) * 100))


def parse_rows(path):
    """Yield one record per feed row.

    record = {"region_code": str, "currency": str, "amount": int (minor units),
              "order_id": str}
    """
    out = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            region = row["region"].strip()
            out.append({
                "region_code": REGION_CODES.get(region, region.lower()),
                "currency": row["currency"].strip().upper(),
                "amount": _to_minor_units(row["amount"]),
                "order_id": row["order_id"].strip(),
            })
    return out
