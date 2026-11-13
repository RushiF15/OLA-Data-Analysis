BUSINESS_QUESTIONS = {
"Which vehicle types generate the most successful bookings?": "SELECT Vehicle_Type, COUNT(*) AS successful_bookings FROM rides WHERE Booking_Status='Success' GROUP BY 1 ORDER BY 2 DESC",
"How much successful booking revenue does each vehicle type generate?": "SELECT Vehicle_Type, SUM(Booking_Value) AS revenue FROM rides WHERE Booking_Status='Success' GROUP BY 1 ORDER BY 2 DESC",
"What is the booking status mix?": "SELECT Booking_Status, COUNT(*) AS bookings FROM rides GROUP BY 1 ORDER BY 2 DESC",
"Which payment methods contribute the most successful revenue?": "SELECT Payment_Method, SUM(Booking_Value) AS revenue FROM rides WHERE Booking_Status='Success' GROUP BY 1 ORDER BY 2 DESC",
"What are the average ride distance and turnaround times by vehicle?": "SELECT Vehicle_Type, AVG(Ride_Distance) AS avg_distance, AVG(V_TAT) AS avg_vehicle_tat, AVG(C_TAT) AS avg_customer_tat FROM rides WHERE Booking_Status='Success' GROUP BY 1 ORDER BY 1",
"Which days have the highest successful booking revenue?": "SELECT Day_Name, SUM(Booking_Value) AS revenue FROM rides WHERE Booking_Status='Success' GROUP BY 1 ORDER BY revenue DESC",
"What are the most common customer cancellation reasons?": "SELECT Canceled_Rides_by_Customer AS reason, COUNT(*) AS cancellations FROM rides WHERE Booking_Status='Canceled by Customer' AND Canceled_Rides_by_Customer IS NOT NULL GROUP BY 1 ORDER BY 2 DESC",
"What are the most common driver cancellation reasons?": "SELECT Canceled_Rides_by_Driver AS reason, COUNT(*) AS cancellations FROM rides WHERE Booking_Status='Canceled by Driver' AND Canceled_Rides_by_Driver IS NOT NULL GROUP BY 1 ORDER BY 2 DESC",
"How many incomplete rides are recorded by reason?": "SELECT Incomplete_Rides_Reason AS reason, COUNT(*) AS rides FROM rides WHERE Incomplete_Rides='Yes' AND NULLIF(TRIM(Incomplete_Rides_Reason),'') IS NOT NULL GROUP BY 1 ORDER BY 2 DESC",
"How do average driver and customer ratings compare by vehicle?": "SELECT Vehicle_Type, AVG(Driver_Ratings) AS avg_driver_rating, AVG(Customer_Rating) AS avg_customer_rating FROM rides WHERE Booking_Status='Success' GROUP BY 1 ORDER BY 1",
}

