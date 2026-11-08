import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")

st.markdown("<h1 style='color:white; background-color:#1a3a5f; padding:15px; border-radius:10px;'>🛒 Ecommerce Sales Dashboard</h1>", unsafe_allow_html=True)
st.write("Report period: Gold Layer | Live from PostgreSQL")

conn = psycopg2.connect(host="127.0.0.1", database="swiggy_db", user="postgres", password="1234", port="5432")
df1 = pd.read_sql("SELECT * FROM gold_category_stats ORDER BY avg_discount DESC LIMIT 10", conn)
df2 = pd.read_sql("SELECT * FROM gold_top_deals ORDER BY discount_percentage DESC LIMIT 10", conn)
conn.close()

# KPI CARDS
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Products", "1351")
c2.metric("Total Categories", "211")
c3.metric("Avg Discount %", f"{df1['avg_discount'].mean():.1f}%")
c4.metric("Max Savings", f"Rs {df2['savings'].max()}")

# CHARTS - 2 side by side
col1, col2 = st.columns(2)
with col1:
    st.subheader("Purchases & Revenue - Avg Discount by Category")
    st.bar_chart(df1.set_index('category')['avg_discount'])

with col2:
    st.subheader("Top Deals - Savings Funnel")
    st.bar_chart(df2.set_index('product_name')['savings'])

st.subheader("Top 10 Deals Table")
st.dataframe(df2, use_container_width=True)