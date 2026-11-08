import pandas as pd
import psycopg2
import re

def clean_price(value):
    # Example: "₹1,099" -> 1099
    if pd.isna(value):
        return None
    text = str(value).replace('₹', '').replace(',', '').strip()
    if text == '' or text == 'nan':
        return None
    try:
        return float(text)
    except:
        return None

def clean_number(value):
    # Example: "64%" -> 64, "24,269" -> 24269
    if pd.isna(value):
        return None
    text = str(value).replace('%', '').replace(',', '').strip()
    if text == '' or text == 'nan':
        return None
    try:
        return float(text)
    except:
        return None

print("Reading Bronze from Postgres...")
conn = psycopg2.connect(
    host="127.0.0.1",
    database="swiggy_db",
    user="postgres",
    password="1234",
    port="5432"
)
df = pd.read_sql("SELECT * FROM bronze_orders", conn)
print(f"Bronze Rows: {len(df)}")

print("Cleaning data...")
df['discounted_price'] = df['discounted_price'].apply(clean_price)
df['actual_price'] = df['actual_price'].apply(clean_price)
df['discount_percentage'] = df['discount_percentage'].apply(clean_number)
df['rating'] = df['rating'].apply(clean_number)
df['rating_count'] = df['rating_count'].apply(clean_number)

# Remove rows where product_id is missing
df = df.dropna(subset=['product_id'])

# Remove duplicates - keep first one
df = df.drop_duplicates(subset=['product_id'])
print(f"Silver Rows after cleaning: {len(df)}")

cur = conn.cursor()
cur.execute("TRUNCATE TABLE silver_orders;")

count = 0
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO silver_orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (row['product_id'], row['product_name'], row['category'],
         row['discounted_price'], row['actual_price'], row['discount_percentage'],
         row['rating'], int(row['rating_count']) if pd.notna(row['rating_count']) else None,
         row['user_id'], row['review_id'])
    )
    count += 1

conn.commit()
print(f"DONE! {count} rows inserted into Silver!")
conn.close()