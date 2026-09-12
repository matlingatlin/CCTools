"""The nightly job."""
import sys
from . import extract, transform, report


def main(feed_path):
    records = extract.parse_rows(feed_path)
    totals = transform.aggregate(records)
    sys.stdout.write(report.render(totals) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
