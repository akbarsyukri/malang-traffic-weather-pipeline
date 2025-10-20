import pandas as pd
import os

# === KONFIGURASI FILE INPUT DAN OUTPUT ===
input_files = {
    "cctv1": r"C:\Users\zoan\snapshots\csv\output_cctv1_with_weather.csv",
    "cctv2": r"C:\Users\zoan\snapshots\csv\output_cctv2_with_weather.csv",
    "cctv3": r"C:\Users\zoan\snapshots\csv\output_cctv3_with_weather.csv"
}
output_dir = r"C:\Users\zoan\snapshots\csv\final_preprocessed"
os.makedirs(output_dir, exist_ok=True)

# === PROSES PRA-PEMROSESAN SETIAP FILE CCTV ===
for cctv, input_path in input_files.items():
    print(f"[INFO] Membaca data untuk {cctv}...")
    df = pd.read_csv(input_path)

    print(f"[INFO] Mengonversi timestamp_str ke datetime untuk {cctv}...")
    df["timestamp"] = pd.to_datetime(df["timestamp_str"], format="%Y%m%d_%H%M%S")

    print(f"[INFO] Mengurutkan berdasarkan timestamp untuk {cctv}...")
    df = df.sort_values(by="timestamp").reset_index(drop=True)

    print(f"[INFO] Jumlah data untuk {cctv}:", len(df))
    print(f"[INFO] Rentang tanggal untuk {cctv}:", df["timestamp"].min(), "sampai", df["timestamp"].max())

    output_path = os.path.join(output_dir, f"dataset_final_{cctv}.csv")
    print(f"[INFO] Menyimpan hasil ke {output_path}...")
    df.to_csv(output_path, index=False)

print("[✔] Pra-pemrosesan semua file selesai.")
