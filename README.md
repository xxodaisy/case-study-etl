# 🏨 Hotel ETL Pipeline
ETL Pipeline untuk mengolah data transaksional hotel dari multiple data source, di-orchestrate menggunakan Luigi.
Project ini dibuat sebagai bagian dari case study BI Engineering pada course Pacmann.

# 📌 Case Description
Sebagai Data Engineer di sebuah hotel, tugas ini adalah membangun ETL Pipeline yang menggabungkan informasi dari beberapa sumber data ke dalam satu tabel analitik (hotel_analysis_table), sehingga memudahkan tim bisnis dalam melakukan analisa data.

# 🗂️ Project Structure
hotel-etl-pipeline/

├── pipeline.py          # Main ETL pipeline (Luigi orchestration)

├── requirements.txt     # Python dependencies

├── README.md            # Project overview (this file)

├── docs/

│   └── technical_documentation.md  # Technical details

└── .gitignore

# 🔌 Data Sources
| Source | Type | Detail |
|--------| -----| -------|
| Payment Data | REST API | https://shandytepe.github.io/payment.json | 
| Customer | PostgreSQL (Docker) | Table customer |
| Reservation | PostgreSQL (Docker) | Table reservation |

# 🔄 Pipeline Overview
ExtractTask → ValidationTask → TransformTask → LoadTask
| Task | Description |
|------| ------------|
| ExtractTask | Ambil data dari API dan PostgreSQL, simpan ke .csv | 
| ValidationTask | Cek shape, tipe data, dan missing values | 
| TransformTask | Join & clean data, simpan ke hotel_analysis_table.csv | 
| LoadTask | UPSERT data ke Data Warehouse (hotel_analysis_db) |

# ⚙️ Setup & Installation
1. Clone repository
bashgit clone https://github.com/username/hotel-etl-pipeline.git
cd hotel-etl-pipeline

2. Buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

4. Setup PostgreSQL (Docker)
Pastikan container PostgreSQL sudah berjalan dengan database pachotel_db.

5. Konfigurasi koneksi database
Edit bagian get_engine() di pipeline.py sesuai kredensial database kamu:
```python
def get_engine():
    return create_engine("postgresql://user:password@localhost:5432/pachotel_db")
```

# ▶️ Menjalankan Pipeline
python pipeline.py
Pipeline akan berjalan secara otomatis setiap 2 menit (loop).
Untuk menghentikan pipeline, tekan Ctrl+C.

# 🗄️ Output
Data hasil transformasi akan di-load ke tabel hotel_analysis_table di database hotel_analysis_db dengan skema berikut:
| Column | Type |
|--------|------|
| reservation_id | INT (Primary Key) |
| customer_id | INT |
| reservation_date | TEXT |
| start_date | TEXT |
| end_date | TEXT |
| total_price | FLOAT |
| review | TEXT |
| rating | INT |
| first_name | TEXT |
| last_name | TEXT |
| email | TEXT |
| phone | TEXT |
| payment_id | INT |
| provider | TEXT |
| account_number | BIGINT |
| payment_status | TEXT |
| payment_date | TEXT |
| expire_date | TEXT |

# 📦 Dependencies
Library utama:

- luigi — pipeline orchestration

- pandas — data manipulation

- sqlalchemy — database connection

- psycopg2 — PostgreSQL adapter

- requests — HTTP API call
