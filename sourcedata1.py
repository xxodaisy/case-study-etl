#import the library
import requests
import pandas as pd

#url JSON payment data
url = "https://shandytepe.github.io/payment.json"

#fetch the data
response = requests.get(url)

#make sure that requests is works
if response.status_code == 200:
 data = response.json()

 #change it to dataframe
 df = pd.DataFrame(data['payment_data'])

 #save to csv
 df.to_csv("payment_data.csv", index=False)
 print(f"Data berhasil disimpan")
else:
 print(f"Gagal mengambil data. Status code:{response.status_code}")
