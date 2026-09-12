"""Stage 2 - convert every record to USD and aggregate per region."""

FX_TO_USD = {
    "USD": 1.0,
    "EUR": 1.09,
    "JPY": 0.0067,
}


def to_usd(record):
    """Convert one record's amount to USD. Returns None if we cannot price it."""
    rate = FX_TO_USD.get(record["currency"])
    if rate is None:
        return None
    return {**record, "amount_usd": record["amount"] * rate}


def aggregate(records):
    """Sum per region. Rows we cannot price are not part of the total."""
    priced = [r for r in (to_usd(rec) for rec in records) if r is not None]
    totals = {}
    for r in priced:
        totals.setdefault(r["region_code"], 0.0)
        totals[r["region_code"]] += r["amount_usd"]
    return [{"region_code": code, "total_usd": total} for code, total in totals.items()]
