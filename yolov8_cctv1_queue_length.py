import os
import cv2
import numpy as np
from shapely.geometry import Point, Polygon
from ultralytics import YOLO
import pandas as pd

# === KONFIGURASI ===
CCTV_ID = "cctv1"
FOLDER = "C:/Users/zoan/snapshots/cctv1"
OUTPUT_DIR = "snapshots/csv"
PROCESSED_DIR = f"C:/Users/zoan/snapshots/processed/{CCTV_ID}"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
OUTPUT_CSV = os.path.join(OUTPUT_DIR, f"output_{CCTV_ID}.csv")

# ROI POLYGON
ROI = Polygon([
    (674, 58),
    (788, 69),
    (1022, 212),
    (721, 200)
])

# ID KENDARAAN (COCO: car, motorbike, bus, truck)
KENDARAAN_IDS = [2, 3, 5, 7]
model = YOLO('yolov8x.pt')

pixel_to_meter = 90 / 149.58  # ≈ 0.602 meter per piksel

hasil = []

for file in sorted(os.listdir(FOLDER)):
    if not file.endswith(".jpg"):
        continue

    path = os.path.join(FOLDER, file)
    frame = cv2.imread(path)

    # === DETEKSI DENGAN CONFIDENCE LEBIH RENDAH ===
    results = model(frame, conf=0.10)
    boxes = results[0].boxes
    kendaraan_dalam_roi = 0
    antrian_points = []

    for box in boxes:
        cls_id = int(box.cls)
        conf_val = float(box.conf)

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        area = (x2 - x1) * (y2 - y1)

        if (
            cls_id in KENDARAAN_IDS and
            conf_val >= 0.10 and
            area > 400 and
            ROI.contains(Point(cx, cy))
        ):
            kendaraan_dalam_roi += 1
            antrian_points.append((cx, cy))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)

    # === GAMBAR ROI ===
    pts = np.array([tuple(map(int, p)) for p in ROI.exterior.coords])
    cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

    # === HITUNG PANJANG ANTRIAN ===
    queue_length_pixel = 0
    if antrian_points:
        y_coords = [pt[1] for pt in antrian_points]
        queue_length_pixel = max(y_coords) - min(y_coords)

    queue_length_meter = round(queue_length_pixel * pixel_to_meter)

    # === TAMPILKAN TEKS ===
    cv2.putText(frame, f"Queue length: {queue_length_meter:.2f}m", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # === SIMPAN HASIL GAMBAR ===
    output_img_path = os.path.join(PROCESSED_DIR, file)
    cv2.imwrite(output_img_path, frame)

    cv2.imshow("Deteksi Kendaraan", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # === CATAT KE CSV ===
    ts = file.replace(f"{CCTV_ID}_", "").replace(".jpg", "")
    hasil.append({
        "timestamp": ts,
        "cctv_id": CCTV_ID,
        "queue_length_meters": queue_length_meter
    })

cv2.destroyAllWindows()

# === SIMPAN FILE CSV ===
df = pd.DataFrame(hasil)
df.to_csv(OUTPUT_CSV, index=False)
print(f"[✔] Data deteksi disimpan ke: {OUTPUT_CSV}")
print(f"[✔] Gambar hasil deteksi disimpan ke: {PROCESSED_DIR}")
