import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from components.charts import bar, line, finish
from config import COLORS
from utils.calculations import successful, money

WEEK_ORDER=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def metric_row(items):
    cols=st.columns(len(items))
    for c,(label,value,help_text) in zip(cols,items):
        c.metric(label,value,help=help_text)

def empty(df):
    if df.empty:
        st.info("No bookings match these filters. Adjust or reset the filters to continue.")
        return True
    return False

def overview(df):
    if empty(df): return
    ok=successful(df)
    rate=(len(ok)/len(df)*100) if len(df) else 0
    metric_row([("Total Bookings",f"{len(df):,}","Bookings in the selected period and filters"),("Successful Bookings",f"{len(ok):,}","Booking_Status = Success"),("Booking Success Rate",f"{rate:.1f}%","Successful bookings divided by all filtered bookings"),("Total Revenue",money(ok.Booking_Value.sum()),"Booking_Value from successful bookings only")])
    st.markdown(" ")
    a,b=st.columns(2)
    counts=df.Vehicle_Type.value_counts().rename_axis("Vehicle_Type").reset_index(name="Bookings")
    a.plotly_chart(bar(counts,"Vehicle_Type","Bookings","Booking Distribution by Vehicle Type"),width="stretch")
    statuses=df.Booking_Status.value_counts().rename_axis("Booking_Status").reset_index(name="Bookings")
    fig=px.pie(statuses,names="Booking_Status",values="Bookings",hole=.58,color_discrete_sequence=COLORS,title="Booking Status Distribution")
    b.plotly_chart(finish(fig,360),width="stretch")
    day=df.assign(Calendar_Date=df.Date.dt.date).groupby("Calendar_Date",as_index=False).size().rename(columns={"size":"Bookings"}).sort_values("Calendar_Date")
    st.plotly_chart(line(day,"Calendar_Date","Bookings","Daily Booking Trends"),width="stretch")
    hour=df.groupby("Hour",as_index=False).size().rename(columns={"size":"Bookings"}).sort_values("Hour")
    st.plotly_chart(line(hour,"Hour","Bookings","Hourly Booking Trends"),width="stretch")

def vehicle(df):
    if empty(df): return
    ok=successful(df); st.caption("Ride metrics and ratings use successful bookings; averages ignore missing values.")
    if ok.empty:
        st.info("No successful bookings match these filters. Select Success in the booking status filter to view vehicle performance.")
        return
    metrics=[("Successful Bookings","Booking_ID","count"),("Average Ride Distance","Ride_Distance","mean"),("Average Vehicle Turnaround Time","V_TAT","mean"),("Average Customer Turnaround Time","C_TAT","mean"),("Average Driver Rating","Driver_Ratings","mean"),("Average Customer Rating","Customer_Rating","mean"),("Total Ride Distance","Ride_Distance","sum")]
    for title,col,agg in metrics:
        data=ok.groupby("Vehicle_Type",as_index=False)[col].agg(agg).rename(columns={col:"Metric"}).sort_values("Metric",ascending=False)
        if agg=="count": data=ok.groupby("Vehicle_Type",as_index=False).size().rename(columns={"size":"Metric"}).sort_values("Metric",ascending=False)
        unit=" (km)" if "Distance" in title else (" (min)" if "Time" in title else (" / 5" if "Rating" in title else ""))
        st.plotly_chart(bar(data,"Vehicle_Type","Metric",title+unit),width="stretch")

def revenue(df):
    if empty(df): return
    ok=successful(df); st.caption("All revenue charts use successful bookings only.")
    if ok.empty:
        st.info("No successful bookings match these filters. Select Success in the booking status filter to view revenue.")
        return
    a,b=st.columns(2)
    byv=ok.groupby("Vehicle_Type",as_index=False).Booking_Value.sum().sort_values("Booking_Value",ascending=False)
    a.plotly_chart(bar(byv,"Vehicle_Type","Booking_Value","Revenue Contribution by Vehicle Type"),width="stretch")
    pay=ok.groupby("Payment_Method",as_index=False).Booking_Value.sum().sort_values("Booking_Value",ascending=False)
    b.plotly_chart(bar(pay,"Payment_Method","Booking_Value","Revenue by Payment Method"),width="stretch")
    daily=ok.assign(Calendar_Date=ok.Date.dt.date).groupby("Calendar_Date",as_index=False).Booking_Value.sum().sort_values("Calendar_Date")
    st.plotly_chart(line(daily,"Calendar_Date","Booking_Value","Daily Revenue Trends"),width="stretch")
    dow=ok.groupby("Day_Name",as_index=False).Booking_Value.sum(); dow["Day_Name"]=pd.Categorical(dow.Day_Name,WEEK_ORDER,ordered=True); dow=dow.sort_values("Day_Name")
    st.plotly_chart(bar(dow,"Day_Name","Booking_Value","Revenue Performance by Day of Week"),width="stretch")
    hourly=ok.groupby("Hour",as_index=False).Booking_Value.sum().sort_values("Hour")
    st.plotly_chart(line(hourly,"Hour","Booking_Value","Hourly Revenue Trends"),width="stretch")
    pv=ok.pivot_table(index="Vehicle_Type",columns="Payment_Method",values="Booking_Value",aggfunc="sum",fill_value=0).reset_index().melt("Vehicle_Type",var_name="Payment_Method",value_name="Revenue")
    fig=px.bar(pv,x="Vehicle_Type",y="Revenue",color="Payment_Method",barmode="group",color_discrete_sequence=COLORS,title="Payment Method Revenue by Vehicle Type")
    st.plotly_chart(finish(fig),width="stretch")

def cancellation(df):
    if empty(df): return
    st.markdown('<div class="note"><b>Source data note:</b> Some rows are marked Incomplete_Rides = Yes while Booking_Status = Success. Original statuses are preserved; incomplete ride analysis uses the explicit incomplete flag and excludes blank reasons.</div>',unsafe_allow_html=True)
    cxl=df[df.Booking_Status.isin(["Canceled by Customer","Canceled by Driver"])].Booking_Status.value_counts().rename_axis("Cancellation Type").reset_index(name="Bookings")
    if cxl.empty:
        st.info("No cancellations match the current booking status filters.")
    else:
        st.plotly_chart(bar(cxl,"Cancellation Type","Bookings","Cancellation Distribution by Type"),width="stretch")
    driver=df[df.Booking_Status.eq("Canceled by Driver")].Canceled_Rides_by_Driver.value_counts().rename_axis("Reason").reset_index(name="Bookings")
    customer=df[df.Booking_Status.eq("Canceled by Customer")].Canceled_Rides_by_Customer.value_counts().rename_axis("Reason").reset_index(name="Bookings")
    a,b=st.columns(2)
    if driver.empty: a.info("No driver cancellations match the filters.")
    else: a.plotly_chart(bar(driver,"Reason","Bookings","Driver Cancellation Reasons",horizontal=True),width="stretch")
    if customer.empty: b.info("No customer cancellations match the filters.")
    else: b.plotly_chart(bar(customer,"Reason","Bookings","Customer Cancellation Reasons",horizontal=True),width="stretch")
    inc=df[df.Incomplete_Rides.eq("Yes")].copy(); inc=inc[inc.Incomplete_Rides_Reason.notna() & inc.Incomplete_Rides_Reason.astype(str).str.strip().ne("")]
    reasons=inc.Incomplete_Rides_Reason.value_counts().rename_axis("Reason").reset_index(name="Rides")
    if reasons.empty: st.info("No incomplete ride reasons are available in this filtered view.")
    else: st.plotly_chart(bar(reasons,"Reason","Rides","Incomplete Rides by Reason"),width="stretch")

def ratings(df):
    if empty(df): return
    metric_row([("Average Driver Rating",f"{df.Driver_Ratings.mean():.2f} / 5","Missing ratings ignored"),("Average Customer Rating",f"{df.Customer_Rating.mean():.2f} / 5","Missing ratings ignored")])
    both=df.groupby("Vehicle_Type",as_index=False)[["Driver_Ratings","Customer_Rating"]].mean().melt("Vehicle_Type",var_name="Rating",value_name="Average Rating")
    both["Rating"]=both.Rating.map({"Driver_Ratings":"Driver","Customer_Rating":"Customer"})
    fig=px.bar(both,x="Vehicle_Type",y="Average Rating",color="Rating",barmode="group",color_discrete_sequence=COLORS,title="Driver vs Customer Ratings by Vehicle Type")
    st.plotly_chart(finish(fig),width="stretch")
    a,b=st.columns(2)
    for c,col,title in [(a,"Driver_Ratings","Driver Rating Distribution"),(b,"Customer_Rating","Customer Rating Distribution")]:
        vals=df[col].dropna(); f=px.histogram(vals,x=col,nbins=10,color_discrete_sequence=[COLORS[0]],title=title); c.plotly_chart(finish(f),width="stretch")
    hourly=df.groupby("Hour",as_index=False)[["Driver_Ratings","Customer_Rating"]].mean().sort_values("Hour")
    st.plotly_chart(line(hourly,"Hour","Driver_Ratings","Average Driver Rating by Hour"),width="stretch")
    st.plotly_chart(line(hourly,"Hour","Customer_Rating","Average Customer Rating by Hour"),width="stretch")


