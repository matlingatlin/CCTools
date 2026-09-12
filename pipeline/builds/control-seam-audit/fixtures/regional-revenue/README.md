# regional-revenue

Nightly job that turns three regional sales feeds into one ranked revenue report.

Three stages, run in order by `revenue/run.py`:

1. `revenue/extract.py`  — read the raw feed rows, normalise them into records
2. `revenue/transform.py` — convert to USD and aggregate per region
3. `revenue/report.py`   — rank the regions and write the summary

Every stage has a unit test suite under `tests/`. Run them with:

    python3 -m unittest discover -s tests -v

`tests/test_transform_fx.py` was added in March after the FX-rate incident, where a
stale rate table made the EMEA figure 12% low for a week. It is the newest and most
thorough suite in the repo.

Last night's run reported APAC as the top region at $41,339,000.00, with North America
last at $11,175,075.00. Finance says APAC did about $0.4M for the period and that North
America was the largest region by a wide margin. All 34 tests pass.

Run the job with:

    python3 -m revenue.run feed.csv
