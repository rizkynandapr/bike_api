from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

# Langsung definisikan nama file jika berada di folder yang sama (root)
CSV_FILE = 'data_cleaned.csv'

def load_data():
    """Membaca CSV dan mengonversinya ke format JSON"""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df.to_dict(orient='records')
    return []

# Memasukkan data ke memori
data_store = load_data()

@app.get("/")
def home():
    # Menampilkan menu lengkap di halaman utama
    return {
        "message": "Bikeshare API Aktif",
        "menu": {
            "lihat_data": "/data",
            "hapus_data": "/data/{index}",
            "dokumentasi_interaktif": "/docs"
        }
    }

@app.get("/data")
def show_all_data():
    """Menampilkan isi CSV secara langsung"""
    if not data_store:
        return {
            "error": "File CSV tidak ditemukan atau kosong",
            "petunjuk": "Pastikan file data_cleaned.csv sudah ada di GitHub"
        }
    return data_store

@app.delete("/data/{index}")
def delete_entry(index: int):
    """Menghapus data sementara di memori"""
    if 0 <= index < len(data_store):
        removed = data_store.pop(index)
        return {
            "status": "success", 
            "message": f"Data index {index} berhasil dihapus",
            "data_terhapus": removed
        }
    raise HTTPException(status_code=404, detail="Index tidak ditemukan")