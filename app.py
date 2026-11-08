import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")

# HEADER - Blue laaga
st.markdown("<div style='background:#1a3a5f; padding:15px; border-radius:10px; color:white;'><h2 style='margin:0;'>Ecommerce sales funnel dashboard</h2><p>Report period: Gold Layer | Live from PostgreSQL</p></div>", unsafe_allow_html=True)
st.write("")

conn = psycopg2.connect(host="127.0.0.1", database="swiggy_db", user="postgres", password="1234", port="5432")
df1 = pd.read_sql("SELECT * FROM gold_category_stats ORDER BY avg_discount DESC LIMIT 10", conn)
df2 = pd.read_sql("SELECT * FROM gold_top_deals ORDER BY discount_percentage DESC LIMIT 10", conn)
conn.close()

# 6 KPI CARDS - photo lo laaga
c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Purchase revenue", "164.4K")
c2.metric("Ecommerce purchases", "3.0K")
c3.metric("Total purchasers", "2.5K")
c4.metric("First time purchasers", "2.0K")
c5.metric("Purchaser rate", "2.6%")
c6.metric("Avg purchase revenue", "1.7")

# ROW 2
col1, col2 = st.columns([2,1])
with col1:
    st.subheader("Purchases & Revenue")
    st.line_chart(df1.set_index('category')['avg_discount'])
with col2:
    st.subheader("Sales funnel (user count)")
    funnel = pd.DataFrame({"stage":["Session start","View product","Add to cart","Begin checkout","Purchases"], "count":[95.6,25.8,9.0,4.1,2.5]})
    fig = px.funnel(funnel, x='count', y='stage', color='stage')
    st.plotly_chart(fig, use_container_width=True)

# ROW 3
col3, col4 = st.columns(2)
with col3:
    st.subheader("Purchasers")
    st.bar_chart(df2.set_index('product_name')['savings'])
with col4:
    st.subheader("Average purchase revenue per active user")
    st.line_chart(df1.set_index('category')['avg_discount'])