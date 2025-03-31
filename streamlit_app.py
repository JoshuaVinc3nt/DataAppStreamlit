import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

# Load data (replace with actual data source)
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

def calculate_profit_margin(sales, profit):
    return (profit / sales) * 100 if sales != 0 else 0

df['Profit_Margin'] = df.apply(lambda row: calculate_profit_margin(row['Sales'], row['Profit']), axis=1)

# Sidebar filters
category = st.selectbox("Select Category", options=df['Category'].unique())
sub_categories = st.multiselect("Select Sub-Categories", options=df[df['Category'] == category]['Sub_Category'].unique())

if sub_categories:
    filtered_df = df[df['Sub_Category'].isin(sub_categories)]
    
    # Ensure Order_Date is in datetime format
    filtered_df["Order_Date"] = pd.to_datetime(filtered_df["Order_Date"])
    
    # Sales Line Chart
    sales_trend = filtered_df.groupby('Order_Date')[['Sales']].sum().reset_index()
    st.line_chart(sales_trend.set_index('Order_Date'))
    
    # Metrics Calculation
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = calculate_profit_margin(total_sales, total_profit)
    
    # Calculate overall profit margin across all products
    overall_avg_margin = calculate_profit_margin(df['Sales'].sum(), df['Profit'].sum())
    
    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{(overall_profit_margin - overall_avg_margin):.2f}%")

st.write("### Input Data and Examples")
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the dataframe index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
