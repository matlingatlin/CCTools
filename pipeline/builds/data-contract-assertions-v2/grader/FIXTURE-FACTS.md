# Fixture facts (the scoring key). Use ONLY to decide the expectations marked [FIXTURE].
Both files hold 4000 rows. Columns: txn_id, merchant, channel, amount, currency, status, customer_age, settled_days.

## Differences that SHOULD stop the batch
- D1_unit_change_amount: column=amount; scope=merchant == belltower only; what=values multiplied by 100 - the feed switched to cents for one merchant; segment_median_reference=32.75; segment_median_current=2726.5; whole_column_median_reference=29.84; whole_column_median_current=33.96; why_it_blocks=a silent unit change is unrecoverable downstream and invisible in a whole-column statistic because it is confined to one segment; rows_affected=440
- D2_null_rate_jump_customer_age: column=customer_age; scope=channel == android; scoped_null_rate_reference=0.0161; scoped_null_rate_current=0.8312; why_it_blocks=a field going missing for one channel is a broken producer, not evolution
- D3_type_drift_settled_days: column=settled_days; non_numeric_rows_current=1184; what=about 30 percent of values arrive as a string with a unit suffix, e.g. '2 d'; why_it_blocks=the column stops being numeric and silently coerces or drops downstream

## Differences that MUST NOT stop the batch
- B1_new_merchant: column=merchant; new_value=harborview; rows=240; why_benign=a real onboarding; the contract should widen, not refuse
- B2_channel_mix_shift: column=channel; what=web share falls and ios rises, same value set; why_benign=a marketing push. Distribution change with no quality fault, and the case a drift test flags loudest
- B3_new_status_value: column=status; new_value=chargeback; rows=90; why_benign=a documented new state, not a corruption

## The fixture's own note
A contract that blocks all six has not solved the problem, it has moved it. A contract that blocks none is decoration. D1 is the hard one: it is confined to one segment and a whole-column check cannot see it.

## A contested figure you must not score against an answer
harborview holds 38 of its 240 rows as whole-number amounts, against 0.41 to 1.48 percent in the seven unaffected merchants and 440 of 440 in belltower. The key above calls harborview purely benign. The CSV supports both readings and independent runs have read it both ways. Do NOT mark an answer down for calling harborview contested, partially affected, or clean - only for asserting one reading with no rival named where expectation E4.4 asks for one.
