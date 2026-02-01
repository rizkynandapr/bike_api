from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

# Fungsi untuk membaca data
def get_data():
    # Mengambil path file CSV yang berada di folder utama (root)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "../data_cleaned.csv")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')
    return []

# Kita simpan ke dalam variabel global agar bisa dimanipulasi (dihapus)
data_store = get_data()

@app.get("/")
def home():
    return {
        "message": "Bikeshare API Berhasil Berjalan",
        "endpoints": {
            "lihat_data": "/data",
            "hapus_data": "/data/{index}"
        }
    }

# ENDPOINT UNTUK MENAMPILKAN SELURUH DATA
@app.get("/data")
def show_all_data():
    if not data_store:
        return {"message": "Data kosong atau file CSV tidak ditemukan"}
    
    return {
        "total_entry": len(data_store),
        "data": data_store
    }

# ENDPOINT UNTUK MENGHAPUS DATA
@app.delete("/data/{index}")
def delete_entry(index: int):
    if 0 <= index < len(data_store):
        item_dihapus = data_store.pop(index)
        return {
            "message": f"Data pada index {index} berhasil dihapus",
            "data_terhapus": item_dihapus,
            "sisa_data": len(data_store)
        }
    else:
        raise HTTPException(status_code=404, detail="Index tidak ditemukan")