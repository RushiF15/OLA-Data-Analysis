# OLA Ride Insights

A Streamlit analytics dashboard for `OLA_Final_Cleaned_Data.csv` in the project root. The source CSV is read in place and is never modified. The dashboard contains seven analytical views, global date/vehicle/status/payment filters, a DuckDB-backed SQL question explorer, and a searchable data explorer.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The app resolves the CSV relative to `app.py`, so it does not depend on the terminal's current directory. If the file is absent, the app shows its expected location and stops; it never substitutes sample data.

## Metric notes

- Revenue and revenue comparisons include only rows where `Booking_Status` is `Success`.
- Vehicle performance metrics use successful bookings. Means ignore missing values.
- Ratings summaries ignore missing ratings.
- Incomplete rides are counted with `Incomplete_Rides = Yes`, excluding empty reasons. The source has records where that flag coexists with `Booking_Status = Success`; both fields are preserved and the cancellation page documents the inconsistency.
- This project folder had no existing SQL notebook or query file. The SQL page therefore provides ten clearly named business questions derived from the available cleaned columns; each query runs against the current filtered data.
- The CSV contains a `Date` column with timestamps. Daily aggregation uses its calendar date.

