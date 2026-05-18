#import the libraries
import luigi
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import time
from pathlib import Path

# #load dotenv
# load_dotenv("pachotel-db.env")

# Otomatis cari .env relatif ke lokasi pipeline.py
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "pachotel-db" / ".env")

def get_engine():
    return create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

#task 1: extract
class ExtractTask(luigi.Task):
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget("extract_data.txt")
    
    def run(self):
        engine = get_engine()
        df_customer = pd.read_sql("SELECT * FROM customer", engine)
        df_reservation = pd.read_sql("SELECT * FROM reservation", engine)
        df_payment = pd.read_sql("SELECT * FROM payment", engine)
        
        df_customer.to_csv("customer.csv", index=False)
        df_reservation.to_csv("reservation.csv", index=False)
        df_payment.to_csv("payment.csv", index=False)
        with self.output().open("w") as f:
            f.write("Data berhasil diekstrak")

#task 2: validation
class ValidationTask(luigi.Task):
    def requires(self):
        return ExtractTask()
    def output(self):
        return luigi.LocalTarget("validation_data.txt")
    def run(self):
        df_customer = pd.read_csv("customer.csv")
        df_reservation = pd.read_csv("reservation.csv")
        df_payment = pd.read_csv("payment.csv")
        
        for df, nama in [(df_customer, "customer"), (df_reservation, "reservation"), (df_payment, "payment")]:
            print(f"\n== {nama} ===")
            print("Shape:", df.shape)
            print("Types:\n", df.dtypes)
            print("Missing values:\n", df.isnull().sum())

        #validasi data
        if df_customer.empty or df_reservation.empty or df_payment.empty:
            raise ValueError("Data tidak boleh kosong")
        
        with self.output().open("w") as f:
            f.write("Data berhasil divalidasi")

#task 3: transform
class TransformTask(luigi.Task):
    def requires(self):
        return ValidationTask() #tunggu validation selesai
    def output(self):
        return luigi.LocalTarget("hotel_analysis_table.csv")
    def run(self):
        df_customer = pd.read_csv("customer.csv")
        df_reservation = pd.read_csv("reservation.csv")
        df_payment = pd.read_csv("payment.csv")

        df_joined = df_reservation.merge(df_customer, on="customer_id", how="left")
        df_final = df_joined.merge(df_payment, on="reservation_id", how="left")

        df_final.drop_duplicates(inplace=True)
        df_final.dropna(subset=["customer_id", "reservation_id"],inplace=True)

        df_final.to_csv("hotel_analysis_table.csv", index=False)
        # with self.output().open("w") as f:
        #     f.write("Data berhasil ditransformasi")

# task 4: load
class LoadTask(luigi.Task):
    def requires(self):
        return TransformTask()
    def output(self):
        return luigi.LocalTarget("load_data.txt")
    def run(self):
        engine = get_engine()
        df_final = pd.read_csv("hotel_analysis_table.csv")

        # Buat tabel dengan primary key kalau belum ada
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS hotel_analysis_table (
                    reservation_id INT PRIMARY KEY,
                    customer_id INT,
                    reservation_date TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    total_price FLOAT,
                    review TEXT,
                    rating INT,
                    created_at_x TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT,
                    created_at_y TEXT,
                    payment_id INT,
                    provider TEXT,
                    account_number BIGINT,
                    payment_status TEXT,
                    payment_date TEXT,
                    expire_date TEXT,
                    created_at TEXT
                )
            """))
            conn.commit()

        # UPSERT per baris
        cols = df_final.columns.tolist()
        update_set = ", ".join([f"{c} = EXCLUDED.{c}" for c in cols if c != "reservation_id"])

        for _, row in df_final.iterrows():
            placeholders = ", ".join([f":{c}" for c in cols])
            query = text(f"""
                INSERT INTO hotel_analysis_table ({", ".join(cols)})
                VALUES ({placeholders})
                ON CONFLICT (reservation_id)
                DO UPDATE SET {update_set}
            """)
            with engine.connect() as conn:
                conn.execute(query, row.to_dict())
                conn.commit()

        with self.output().open("w") as f:
            f.write(f"Data berhasil dimuat. Jumlah baris: {df_final.shape[0]}")


# run pipeline
if __name__ == "__main__":
    while True:
        # hapus marker files biar pipeline run ulang
        for file in ["extract_data.txt", "validation_data.txt", "hotel_analysis_table.csv", "load_data.txt"]:
            if os.path.exists(file):
                os.remove(file)

        luigi.build([LoadTask()], local_scheduler=True)
        print("Pipeline selesai. Tunggu 2 menit...")
        time.sleep(120)