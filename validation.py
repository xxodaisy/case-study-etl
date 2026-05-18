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

#validate data
def validate(df, customer):
    #check null values
    null_values = df.isnull().sum()
    print(f"Null values in {customer}:\n{null_values}\n")
    #check duplicates
    duplicates = df.duplicated().sum()
    print(f"Duplicate values in {customer}: {duplicates}\n")
    #check data types
    data_types = df.dtypes
    print(f"Data types in {customer}:\n{data_types}\n")
    #check unique values
    unique_values = df.nunique()
    print(f"Unique values in {customer}:\n{unique_values}\n")
    #check data shape
    shape = df.shape
    print(f"Shape of {customer}: {shape}\n")

def validate(df, reservation):
    #check null values
    null_values = df.isnull().sum()
    print(f"Null values in {reservation}:\n{null_values}\n")
    #check duplicates
    duplicates = df.duplicated().sum()
    print(f"Duplicate values in {reservation}: {duplicates}\n")
    #check data types
    data_types = df.dtypes
    print(f"Data types in {reservation}:\n{data_types}\n")
    #check unique values
    unique_values = df.nunique()
    print(f"Unique values in {reservation}:\n{unique_values}\n")
    #check data shape
    shape = df.shape
    print(f"Shape of {reservation}: {shape}\n")

def validate(df, payment):
    #check null values
    null_values = df.isnull().sum()
    print(f"Null values in {payment}:\n{null_values}\n")
    #check duplicates
    duplicates = df.duplicated().sum()
    print(f"Duplicate values in {payment}: {duplicates}\n")
    #check data types
    data_types = df.dtypes
    print(f"Data types in {payment}:\n{data_types}\n")
    #check unique values
    unique_values = df.nunique()
    print(f"Unique values in {payment}:\n{unique_values}\n")
    #check data shape
    shape = df.shape
    print(f"Shape of {payment}: {shape}\n")

validate(df_customer, "customer")
validate(df_reservation, "reservation")
validate(df_payment, "payment")
