import pandas as pd
import streamlit as st
from config import DATA_PATH

@st.cache_data(show_spinner="Loading ride dataâ€¦")
def load_data():
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"The cleaned dataset was not found at {DATA_PATH}. Place OLA_Final_Cleaned_Data.csv beside app.py.")
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time
    return df


