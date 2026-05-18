import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#load .env
load_dotenv("pachotel-db/.env")

#connect to database
engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

#load data
df_customer = pd.read_sql("SELECT * FROM customer", engine)
df_reservation = pd.read_sql("SELECT * FROM reservation", engine)
df_payment = pd.read_sql("SELECT * FROM payment", engine)

#join data
df_joined = df_reservation.merge(df_customer, on="customer_id", how="left")
df_final = df_joined.merge(df_payment, on="reservation_id", how="left")

#cleaning data
#drop duplicates
df_final.drop_duplicates(inplace=True)

#drop baris yg missing values di kolom penting
df_final.dropna(subset=["customer_id", "reservation_id", "payment_id"], inplace=True)

#save hasil transformasi 
print("Data berhasil ditransformasi:", df_final.shape)
print(df_final.head())

#load to csv
df_final.to_csv("hotel_analysis_table.csv", index=False)
print("Data berhasil disimpan ke hotel_analysis_table.csv")

