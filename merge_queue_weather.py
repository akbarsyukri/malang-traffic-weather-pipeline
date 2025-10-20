import pandas as pd

# === LOAD DATASET PER CCTV DAN CUACA ===
df_cctv1 = pd.read_csv("C:/Users/zoan/snapshots/csv/output_cctv1.csv")
df_cctv2 = pd.read_csv("C:/Users/zoan/snapshots/csv/output_cctv2.csv")
df_cctv3 = pd.read_csv("C:/Users/zoan/snapshots/csv/output_cctv3.csv")
df_cuaca = pd.read_csv("C:/Users/zoan/snapshots/csv/cuaca_openweather.csv")

# === KONVERSI TIMESTAMP KE DATETIME ===
for df in [df_cctv1, df_cctv2, df_cctv3, df_cuaca]:
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d_%H%M%S")

# === BULATKAN TIMESTAMP KE JAM TERDEKAT UNTUK MERGE ===
for df in [df_cctv1, df_cctv2, df_cctv3, df_cuaca]:
    df["timestamp_hour"] = df["timestamp"].dt.floor("h")

# === URUTKAN UNTUK MERGE_ASOF ===
df_cctv1 = df_cctv1.sort_values("timestamp_hour")
df_cctv2 = df_cctv2.sort_values("timestamp_hour")
df_cctv3 = df_cctv3.sort_values("timestamp_hour")
df_cuaca = df_cuaca.sort_values("timestamp_hour")

# === FUNGSI GABUNG DENGAN CUACA ===
def merge_with_weather(df_kendaraan, df_cuaca):
    merged = pd.merge_asof(
        left=df_kendaraan,
        right=df_cuaca.drop(columns=["timestamp"]),  # Hindari duplikasi kolom timestamp
        on="timestamp_hour",
        direction="backward"
    )
    merged["timestamp_str"] = merged["timestamp"].dt.strftime("%Y%m%d_%H%M%S")
    return merged.sort_values(["timestamp", "cctv_id"])

# === GABUNGKAN MASING-MASING CCTV DENGAN CUACA ===
df1_final = merge_with_weather(df_cctv1, df_cuaca)
df2_final = merge_with_weather(df_cctv2, df_cuaca)
df3_final = merge_with_weather(df_cctv3, df_cuaca)

# === PILIH KOLOM YANG DIBUTUHKAN ===
columns_final = [
    "timestamp_str", "cctv_id", "queue_length_meters",
    "temperature", "humidity", "weather", "wind_speed"
]
df1_final = df1_final[columns_final]
df2_final = df2_final[columns_final]
df3_final = df3_final[columns_final]

# === SIMPAN HASIL GABUNGAN KE FILE CSV ===
df1_final.to_csv("output_cctv1_with_weather.csv", index=False)
df2_final.to_csv("output_cctv2_with_weather.csv", index=False)
df3_final.to_csv("output_cctv3_with_weather.csv", index=False)

print("[✔] File hasil telah disimpan:")
print(" - output_cctv1_with_weather.csv")
print(" - output_cctv2_with_weather.csv")
print(" - output_cctv3_with_weather.csv")
