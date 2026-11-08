import pandas as pd
import psycopg2

print("Reading CSV...")
df = pd.read_csv("Amazon_Sales.csv")
print(f"Total Rows: {len(df)}")

conn = psycopg2.connect(
    host="127.0.0.1",
    database="swiggy_db",
    user="postgres",
    password="1234",
    port="5432"
)
print("Postgres Connected!")
cur = conn.cursor()

cur.execute("TRUNCATE TABLE bronze_orders;")

print("Inserting into Bronze...")
count = 0
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO bronze_orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (str(row['product_id']), str(row['product_name'])[:200], str(row['category']),
         str(row['discounted_price']), str(row['actual_price']), str(row['discount_percentage']),
         str(row['rating']), str(row['rating_count']), str(row['user_id']), str(row['review_id']))
    )
    count += 1

conn.commit()
print(f"DONE! Really inserted {count} rows into Bronze!")
conn.close()