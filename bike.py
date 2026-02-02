from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

# Pengaturan lokasi file CSV
CSV_FILE = 'data_cleaned.csv'

def load_initial_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df.to_dict(orient='records')
    return []

# State management dalam memori (serverless)
data_store = load_initial_data()
deleted_history = [] # Variabel untuk menampung data yang dihapus

@app.get("/")
def welcome_page():
    return {
        "message": "Bikeshare API",
        "status": "Online",
        "menu_navigasi": {
            "lihat_semua_data": "/tampilkan-data",
            "cek_riwayat_hapus": "/riwayat-hapus",
            "dokumentasi_interaktif": "/docs"
        }
    }

@app.get("/tampilkan-data")
def get_cleaned_trips():
    """Menampilkan seluruh entry data setelah handling outlier"""
    return {
        "keterangan": "Data Aktif",
        "jumlah_data": len(data_store),
        "data": data_store
    }

@app.get("/riwayat-hapus")
def get_deleted_log():
    """Menampilkan data apa saja yang sudah dihapus selama session ini"""
    return {
        "keterangan": "Riwayat Data Terhapus",
        "jumlah_terhapus": len(deleted_history),
        "data": deleted_history
    }

@app.delete("/hapus-data/{index}")
def remove_trip_entry(index: int):
    """Menghapus entry data dan memindahkannya ke riwayat hapus"""
    if 0 <= index < len(data_store):
        # Proses pemindahan data
        removed_item = data_store.pop(index)
        deleted_history.append(removed_item)
        
        return {
            "status": "Berhasil Dihapus",
            "item": removed_item,
            "pesan": "Data telah dipindahkan ke /riwayat-hapus"
        }
    else:
        raise HTTPException(status_code=404, detail="Index data tidak ditemukan")