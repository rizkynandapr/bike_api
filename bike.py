from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

# Gunakan path relatif agar aman di server Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "../data_cleaned.csv")

try:
    df = pd.read_csv(csv_path)
    data_list = df.to_dict(orient='records')
except Exception as e:
    data_list = []

@app.get("/")
def root():
    return {"message": "API Bikeshare Berhasil di Deploy ke Vercel"}

@app.get("/data")
def get_all():
    return data_list

@app.delete("/data/{index}")
def delete_item(index: int):
    if 0 <= index < len(data_list):
        removed = data_list.pop(index)
        return {"status": "deleted", "item": removed}
    raise HTTPException(status_code=404, detail="Index out of range")