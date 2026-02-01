from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

# Lokasi file CSV hasil olahan Colab
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data_cleaned.csv')

def load_data():
    """Membaca CSV dan mengonversinya ke format JSON (List of Dict)"""
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return df.to_dict(orient='records')
    return []

# Memasukkan data ke memori saat API pertama kali dijalankan
data_store = load_data()

@app.get("/")
def home():
    return {"message": "Bikeshare API Aktif", "menu": "/data"}

@app.get("/data")
def show_all_data():
    """Menampilkan isi CSV secara langsung"""
    if not data_store:
        # Jika muncul pesan ini, periksa apakah file data_cleaned.csv sudah di-push ke GitHub
        return {"error": "File CSV tidak ditemukan atau kosong di server"}
    
    return data_store

@app.delete("/data/{index}")
def delete_entry(index: int):
    """Menghapus data sementara di memori"""
    if 0 <= index < len(data_store):
        removed = data_store.pop(index)
        return {"status": "success", "data_terhapus": removed}
    raise HTTPException(status_code=404, detail="Index tidak ditemukan")