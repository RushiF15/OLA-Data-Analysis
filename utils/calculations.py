import pandas as pd

def apply_filters(df, date_range=None, vehicles=None, statuses=None, payments=None):
    out = df
    if date_range and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        out = out[out.Date.between(start, end + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1))]
    if vehicles is not None: out = out[out.Vehicle_Type.isin(vehicles)]
    if statuses is not None: out = out[out.Booking_Status.isin(statuses)]
    if payments is not None: out = out[out.Payment_Method.isin(payments)]
    return out

def successful(df):
    return df[df.Booking_Status.eq("Success")]

def money(value):
    return f"â‚¹{value:,.0f}"


