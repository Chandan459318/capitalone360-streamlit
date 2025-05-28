# app.py

import os
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql  # Needed for pymysql to work with SQLAlchemy
import matplotlib.pyplot as plt

# Database connection
username = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'capitalone360'

# Create SQLAlchemy engine with pymysql
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Read data from MySQL
query = "SELECT * FROM capitalone360.capitalone_mock_transactions"  # Replace 'transactions' with your table name if different
df = pd.read_sql(query, con=engine)

# Load fraud-detected transactions
fraud_query = "SELECT * FROM capitalone360.capitalone_fraud_detected"
fraud_df = pd.read_sql(fraud_query, con=engine)

# ------------------ Load Segmentation Data ------------------
segment_query = "SELECT * FROM capitalone360.capitalone_user_segments"
segment_df = pd.read_sql(segment_query, con=engine)

# Merge with main data (assuming df is your main transaction DataFrame)
df = df.merge(segment_df, on='User_ID', how='left')


# Page setup
st.set_page_config(page_title="CapitalOne360 Dashboard", layout="wide")
st.title("💳 CapitalOne360 Financial Insights Dashboard")

# Sidebar filters
st.sidebar.header("📊 Filters")
selected_user = st.sidebar.multiselect("User ID", df["User_ID"].unique())
selected_category = st.sidebar.multiselect("Category", df["Category"].unique())
selected_city = st.sidebar.multiselect("City", df["City"].unique())

# Apply filters
filtered_df = df.copy()
if selected_user:
    filtered_df = filtered_df[filtered_df["User_ID"].isin(selected_user)]
if selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]
if selected_city:
    filtered_df = filtered_df[filtered_df["City"].isin(selected_city)]

# KPIs
total_spend = filtered_df["Amount"].sum()
avg_spend = filtered_df["Amount"].mean()
unique_users = filtered_df["User_ID"].nunique()
num_transactions = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend ($)", f"{total_spend:,.2f}")
col2.metric("Average Spend ($)", f"{avg_spend:,.2f}")
col3.metric("Unique Users", unique_users)
col4.metric("Total Transactions", num_transactions)

# Charts
filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
filtered_df["Month"] = filtered_df["Date"].dt.to_period("M")

monthly_spend = filtered_df.groupby("Month")["Amount"].sum()
category_spend = filtered_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
merchant_counts = filtered_df["Merchant"].value_counts().head(10)

st.subheader("📈 Monthly Spend Trend")
st.bar_chart(monthly_spend)

st.subheader("🛒 Spend by Category")
st.bar_chart(category_spend)

st.subheader("🏬 Top 10 Merchants by Transaction Count")
st.bar_chart(merchant_counts)

# Data table
#st.subheader("🧾 Transactions Table")
#st.dataframe(filtered_df)



# Done!
st.success("Dashboard loaded successfully ✅")






# Data table
st.subheader("🧾 Transactions Table")
st.dataframe(filtered_df)

# Export CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_transactions.csv',
    mime='text/csv'
)

st.subheader("👥 User-Level Spend Summary")
user_summary = filtered_df.groupby("User_ID")["Amount"].agg(['count', 'sum', 'mean']).reset_index()
user_summary.columns = ["User_ID", "Transaction Count", "Total Spend ($)", "Avg Spend ($)"]
st.dataframe(user_summary.sort_values("Total Spend ($)", ascending=False))

top_merchant = st.selectbox("🔍 View Transactions for Top Merchant", df["Merchant"].value_counts().head(10).index)
merchant_df = filtered_df[filtered_df["Merchant"] == top_merchant]
st.write(f"📄 Transactions from **{top_merchant}**")
st.dataframe(merchant_df)






st.markdown("---")
st.subheader("🚨 Fraud Detection Insights")

fraud_df['Date'] = pd.to_datetime(fraud_df['Date'])
fraud_df['Fraud_Risk'] = fraud_df['Fraud_Risk'].astype(str) == 'True'

st.metric("⚠️ Total Fraud-Suspected Transactions", fraud_df['Fraud_Risk'].sum())

flag_cols = ['High_Amount_Flag', 'Rapid_Transaction_Flag', 'City_Change_Flag', 'Anomaly_Flag']
for col in flag_cols:
    fraud_df[col] = fraud_df[col].astype(str) == 'True'
    st.write(f"🔹 `{col}`: {fraud_df[col].sum()} flagged")

st.dataframe(fraud_df[fraud_df['Fraud_Risk'] == True].sort_values(by='Date', ascending=False))




# ------------------ Streamlit UI: Segmentation ------------------
st.markdown("## 🧩 User Segmentation Insights")

# Segment counts
segment_counts = df['User_Segment'].value_counts().sort_index()

# Display metrics per segment
for seg in sorted(segment_counts.index):
    st.metric(f"Segment {seg}", f"{segment_counts[seg]} users")

# Average spend per segment
avg_spend_by_segment = df.groupby("User_Segment")["Amount"].mean().round(2)
st.bar_chart(avg_spend_by_segment)

# Transactions by segment table
st.subheader("🔍 Sample Transactions by Segment")
selected_segment = st.selectbox("Choose Segment to View Transactions", sorted(df['User_Segment'].dropna().unique()))
segment_transactions = df[df["User_Segment"] == selected_segment]
st.dataframe(segment_transactions)







# -------------------------
# 📦 Smart Recommendations
# -------------------------
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

st.markdown("### 🧠 Smart Merchant Recommendations")

# Load transactions and user segments from MySQL
transactions_query = "SELECT * FROM capitalone360.capitalone_mock_transactions"
segments_query = "SELECT * FROM capitalone360.capitalone_user_segments"
tx_df = pd.read_sql(transactions_query, con=engine)
user_segments_df = pd.read_sql(segments_query, con=engine)

# Compute user-merchant matrix
pivot_df = tx_df.pivot_table(index='User_ID', columns='Merchant', values='Amount', aggfunc='mean', fill_value=0)

# Compute cosine similarity between users
user_similarity = pd.DataFrame(cosine_similarity(pivot_df), 
                                index=pivot_df.index, 
                                columns=pivot_df.index)

# Function to get recommended merchants for a user
def get_recommendations(user_id, top_n=5):
    if user_id not in pivot_df.index:
        return pd.Series([], name="Merchant")

    similar_users = user_similarity[user_id].sort_values(ascending=False)[1:]  # exclude self
    weights = similar_users / similar_users.sum()

    weighted_avg = pivot_df.loc[similar_users.index].T.dot(weights)
    already_visited = pivot_df.loc[user_id]
    recommendations = weighted_avg[already_visited == 0].sort_values(ascending=False)
    
    return recommendations.head(top_n)

# UI Dropdown to choose user
selected_user_id = st.selectbox("Select a User to Recommend Merchants", options=pivot_df.index)

# Show recommendations
if selected_user_id:
    st.subheader(f"Recommended merchants for User {selected_user_id}:")
    recs = get_recommendations(selected_user_id)
    st.table(recs.rename("Estimated Spend ($)").reset_index().rename(columns={"index": "Merchant"}))
