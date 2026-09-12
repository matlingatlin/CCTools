"""Stage 3 - rank the regions and render the summary."""

DISPLAY = {"na": "North America", "emea": "EMEA", "apac": "APAC"}


def _amount(row):
    # transform used to emit "total"; it emits "total_usd" since the currency
    # work. Accept both so old saved runs still render.
    if "total_usd" in row:
        return row["total_usd"]
    return row.get("total", 0)


def rank(rows):
    """Highest revenue first."""
    return sorted(rows, key=lambda r: r.get("total", 0), reverse=True)


def render(rows):
    ranked = rank(rows)
    lines = ["Regional revenue, highest first", ""]
    for i, r in enumerate(ranked, 1):
        name = DISPLAY.get(r["region_code"], r["region_code"])
        lines.append("%d. %-15s $%.2f" % (i, name, _amount(r)))
    lines.append("")
    lines.append("Top region: %s" % DISPLAY.get(ranked[0]["region_code"], "?"))
    return "\n".join(lines)
