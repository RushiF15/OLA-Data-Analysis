import streamlit as st
from components.styles import inject_css
from config import APP_TITLE, NAV_ITEMS
from utils.data_loader import load_data
from utils.calculations import apply_filters
from utils.sql_queries import BUSINESS_QUESTIONS
from pages import dashboard_pages as pages

st.set_page_config(page_title=APP_TITLE, page_icon="â—ˆ", layout="wide", initial_sidebar_state="expanded")
inject_css()

try:
    df=load_data()
except Exception as exc:
    st.error(str(exc)); st.stop()

with st.sidebar:
    st.markdown('<p class="brand">O<em>LA</em></p><div class="eyebrow">Ride Intelligence</div>',unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown('<div class="section-label">Workspace</div>',unsafe_allow_html=True)
    selected=st.radio("Dashboard navigation",NAV_ITEMS,label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="section-label">Global filters</div>',unsafe_allow_html=True)
    min_d,max_d=df.Date.min().date(),df.Date.max().date()
    date_range=st.date_input("Date range",value=(min_d,max_d),min_value=min_d,max_value=max_d,key="global_dates")
    vehicle_values=sorted(df.Vehicle_Type.dropna().unique().tolist())
    status_values=sorted(df.Booking_Status.dropna().unique().tolist())
    payment_values=sorted(df.Payment_Method.dropna().unique().tolist())
    vehicles=st.multiselect("Vehicle type",vehicle_values,default=vehicle_values,key="global_vehicles")
    statuses=st.multiselect("Booking status",status_values,default=status_values,key="global_statuses")
    payments=st.multiselect("Payment method",payment_values,default=payment_values,key="global_payments")
    if st.button("Reset filters",width="stretch"):
        for key in ("global_dates","global_vehicles","global_statuses","global_payments"):
            st.session_state.pop(key,None)
        st.rerun()
    st.markdown("---")
    st.caption("OLA Ride Insights Â· Business Intelligence\n\nSource: cleaned ride bookings dataset")

filtered=apply_filters(df,date_range,vehicles,statuses,payments)

st.markdown('<div class="eyebrow">OLA RIDE INSIGHTS</div>',unsafe_allow_html=True)
st.title(selected)
st.markdown('<div class="subhead">Data Analytics & Business Intelligence Dashboard</div>',unsafe_allow_html=True)
st.caption(f"Dataset coverage: {min_d:%d %b %Y} â€” {max_d:%d %b %Y}  Â·  {len(filtered):,} of {len(df):,} bookings in current view")
st.markdown(" ")

if selected=="Overview": pages.overview(filtered)
elif selected=="Vehicle Analysis": pages.vehicle(filtered)
elif selected=="Revenue Analysis": pages.revenue(filtered)
elif selected=="Cancellation Analysis": pages.cancellation(filtered)
elif selected=="Ratings Analysis": pages.ratings(filtered)
elif selected=="SQL Query Explorer":
    st.markdown("Explore a set of business questions against the currently filtered source data.")
    question=st.selectbox("Business question",list(BUSINESS_QUESTIONS))
    query=BUSINESS_QUESTIONS[question]
    st.code(query,language="sql")
    try:
        try:
            import duckdb
            con=duckdb.connect(database=":memory:")
            con.register("rides",filtered)
            result=con.execute(query).df()
            engine="DuckDB"
            con.close()
        except ImportError:
            # Portable local SQL fallback when DuckDB is not installed in the current environment.
            import sqlite3
            con=sqlite3.connect(":memory:")
            filtered.to_sql("rides",con,index=False,if_exists="replace")
            result=__import__("pandas").read_sql_query(query,con)
            engine="SQLite fallback"
            con.close()
        st.markdown(f"**{len(result):,} result rows** Â· Query ran against {len(filtered):,} filtered bookings")
        st.caption(f"Execution engine: {engine}")
        st.dataframe(result,width="stretch",hide_index=True)
        if len(result)>0 and len(result.columns)>=2 and result.iloc[:,1].dtype.kind in "if":
            st.plotly_chart(pages.bar(result,result.columns[0],result.columns[1],question),width="stretch")
    except Exception as exc:
        st.error(f"Could not execute this query: {exc}")
elif selected=="Data Explorer":
    st.markdown("#### Dataset profile")
    a,b,c=st.columns(3); a.metric("Rows",f"{len(filtered):,}"); b.metric("Columns",f"{filtered.shape[1]}"); c.metric("Missing cells",f"{int(filtered.isna().sum().sum()):,}")
    with st.expander("Missing-value summary",expanded=False):
        missing=filtered.isna().sum().rename("Missing values").to_frame(); missing["Missing %"]=(missing["Missing values"]/max(len(filtered),1)*100).round(1)
        missing=missing[missing["Missing values"]>0].sort_values("Missing values",ascending=False)
        if missing.empty: st.success("No missing values in the current view.")
        else: st.dataframe(missing,width="stretch")
    query=st.text_input("Search rows",placeholder="Search any text value, for example a location or booking ID")
    view=filtered
    if query.strip():
        mask=view.astype("string").apply(lambda col: col.str.contains(query.strip(),case=False,na=False,regex=False)).any(axis=1)
        view=view[mask]
    st.caption(f"Showing {len(view):,} matching records")
    st.dataframe(view,width="stretch",hide_index=True,height=540)
    st.download_button("Download filtered data as CSV",data=view.to_csv(index=False).encode("utf-8"),file_name="ola_filtered_rides.csv",mime="text/csv")


