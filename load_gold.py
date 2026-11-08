import pandas as pd
import psycopg2

print("Reading Silver...")
conn = psycopg2.connect(
    host="127.0.0.1",
    database="swiggy_db",
    user="postgres",
    password="1234",
    port="5432"
)
df = pd.read_sql("SELECT * FROM silver_orders", conn)
print(f"Silver Rows: {len(df)}")

# Create savings column
df['savings'] = df['actual_price'] - df['discounted_price']

# 1. Category Stats
print("Building Gold Category Stats...")
category_stats = df.groupby('category').agg(
    total_products=('product_id', 'count'),
    avg_discount=('discount_percentage', 'mean'),
    avg_rating=('rating', 'mean'),
    avg_discounted_price=('discounted_price', 'mean'),
    total_savings=('savings', 'sum')
).reset_index().round(2)

# 2. Top 10 Deals
print("Building Gold Top Deals...")
top_deals = df.sort_values(by='discount_percentage', ascending=False).head(10)
top_deals = top_deals[['product_name', 'category', 'discounted_price', 'actual_price', 'discount_percentage', 'savings', 'rating']]

cur = conn.cursor()
cur.execute("TRUNCATE TABLE gold_category_stats;")
cur.execute("TRUNCATE TABLE gold_top_deals;")

for _, row in category_stats.iterrows():
    cur.execute("INSERT INTO gold_category_stats VALUES (%s,%s,%s,%s,%s,%s)",
                (row['category'], int(row['total_products']), float(row['avg_discount']),
                 float(row['avg_rating']), float(row['avg_discounted_price']), float(row['total_savings'])))

for _, row in top_deals.iterrows():
    cur.execute("INSERT INTO gold_top_deals VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (row['product_name'], row['category'], float(row['discounted_price']),
                 float(row['actual_price']), float(row['discount_percentage']),
                 float(row['savings']), float(row['rating'])))

conn.commit()
print(f"DONE! Gold Category: {len(category_stats)} rows")
print(f"DONE! Gold Top Deals: {len(top_deals)} rows")
conn.close()