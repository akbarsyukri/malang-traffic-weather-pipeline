import cv2
import time
import os
import concurrent.futures
import requests
import pandas as pd
from datetime import datetime

# === KONFIGURASI STREAM CCTV ===
streams = {
    "cctv1": "http://stream.cctv.malangkota.go.id/WebRTCApp/streams/307023650278212238808482.m3u8?token=null",
    "cctv2": "http://stream.cctv.malangkota.go.id/WebRTCApp/streams/982131430615781858979987.m3u8?token=null",
    "cctv3": "http://stream.cctv.malangkota.go.id/WebRTCApp/streams/719653317344542196173839.m3u8?token=null",
}

interval_snapshot = 60  # Snapshot setiap 60 detik (1 menit)
interval_weather = 5  # Request cuaca setiap 5 menit

# === JAM AKTIF (06:00 - 18:00) ===
def is_within_active_hours():
    now = datetime.now().time()
    return datetime.strptime("06:00", "%H:%M").time() <= now <= datetime.strptime("18:00", "%H:%M").time()

# === KONFIGURASI CUACA ===
API_KEY = "63ed0c7e98dae204c75c5d3827f1be3b"
LAT, LON = -7.9404733, 112.642453
CUACA_CSV = "cuaca_openweather.csv"

# === TRACK JAM TERAKHIR DATA CUACA DISIMPAN ===
last_weather_minute = None

def ambil_dan_simpan_cuaca():
    global last_weather_minute
    now = datetime.now()

    # Cek hanya jam tertentu dan menit kelipatan 5
    if now.minute % 5 != 0 or (now.hour == 18 and now.minute > 0):
        return

    # Cek apakah cuaca sudah disimpan pada menit ini
    if now.minute == last_weather_minute:
        return

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if "main" in response and "weather" in response:
            data = {
                "timestamp": now.strftime("%Y%m%d_%H%M%S"),
                "temperature": response["main"]["temp"],
                "humidity": response["main"]["humidity"],
                "weather": response["weather"][0]["main"],
                "wind_speed": response["wind"]["speed"]
            }

            df = pd.DataFrame([data])
            df.to_csv(CUACA_CSV, mode="a", header=not os.path.exists(CUACA_CSV), index=False)
            last_weather_minute = now.minute  # tandai sudah simpan menit ini
            print(f"[🌦] Cuaca tersimpan: {data}")
        else:
            print("[✘] Response cuaca tidak valid:", response)

    except Exception as e:
        print(f"[✘] Error ambil cuaca: {e}")

# === BUAT FOLDER UNTUK SETIAP CCTV ===
for cam_id in streams:
    os.makedirs(f"snapshots/{cam_id}", exist_ok=True)

# === FUNGSI PENGAMBILAN STREAM PER CCTV ===
def capture_stream(cam_id, url):
    print(f"[INFO] Memulai stream untuk {cam_id}")
    
    while True:
        if is_within_active_hours():
            cap = cv2.VideoCapture(url)
            time.sleep(2)  # beri waktu buffer
            ret, frame = cap.read()
            if ret:
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"snapshots/{cam_id}/{cam_id}_{now}.jpg"
                cv2.imwrite(filename, frame)
                print(f"[✔] {cam_id} saved: {filename}")

                # Ambil cuaca hanya oleh CCTV1
                if cam_id == "cctv1":
                    ambil_dan_simpan_cuaca()
            else:
                print(f"[✘] Gagal membaca frame dari {cam_id}")
            cap.release()
        else:
            print(f"[⏸] {cam_id} di luar jam aktif, menunggu...")

        time.sleep(interval_snapshot)

# === JALANKAN SEMUA CCTV SECARA PARALEL ===
if __name__ == "__main__":
    print("[INFO] Menjalankan semua stream CCTV (snapshot tiap 1 menit)...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for cam_id, url in streams.items():
            executor.submit(capture_stream, cam_id, url)
