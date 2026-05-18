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

#load dari csv hasil transform
df_final = pd.read_csv("hotel_analysis_table.csv")

#load to data warehouse
df_final.to_sql("hotel_analysis_table", engine, if_exists="replace", index=False)
print("Data berhasil dimuat ke data warehouse. Jumlah baris:", df_final.shape[0])