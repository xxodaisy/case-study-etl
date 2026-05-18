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

#extract data from database
df_customer = pd.read_sql("SELECT * FROM customer", engine)
df_reservation = pd.read_sql("SELECT * FROM reservation", engine)
df_room = pd.read_sql("SELECT * FROM room", engine)
df_payment = pd.read_sql("SELECT * FROM payment", engine)
df_reservation_room = pd.read_sql("SELECT * FROM reservation_room", engine)

#load payment from CSV hasil sourcedata1.py
df_payment = pd.read_csv("payment_data.csv")

print("customer:", df_customer.shape)
print("reservation:", df_reservation.shape)
print("room:", df_room.shape)
print("payment:", df_payment.shape)
print("reservation_room:", df_reservation_room.shape)
