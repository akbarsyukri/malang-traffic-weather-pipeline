import pandas as pd
import os

# === KONFIGURASI FILE INPUT DAN OUTPUT ===
input_files = {
    "cctv1": r"C:\Users\zoan\snapshots\csv\final_preprocessed\dataset_final_cctv1.csv",
    "cctv2": r"C:\Users\zoan\snapshots\csv\final_preprocessed\dataset_final_cctv2.csv",
    "cctv3": r"C:\Users\zoan\snapshots\csv\final_preprocessed\dataset_final_cctv3.csv"
}
output_dir = r"C:\Users\zoan\snapshots\csv\final_jam_menit"
os.makedirs(output_dir, exist_ok=True)

# === PROSES SETIAP FILE CCTV ===
for cctv, input_path in input_files.items():
    print(f"[INFO] Membaca dan memproses data {cctv}...")
    df = pd.read_csv(input_path)
    
    # Konversi timestamp dan set detik menjadi 00
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].dt.floor('min')

    # Format ulang timestamp tanpa detik (YYYY-MM-DD HH:MM)
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')

    # Simpan hasil ke file baru
    output_path = os.path.join(output_dir, f"dataset_final_{cctv}.csv")
    df.to_csv(output_path, index=False)
    print(f"[✔] File disimpan: {output_path}")

print("[✅] Semua file berhasil diproses dan timestamp diatur ke format jam dan menit.")
