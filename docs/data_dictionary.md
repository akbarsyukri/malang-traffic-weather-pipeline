# Data Dictionary (excerpt)
All timestamps use ISO-8601 (`YYYY-MM-DD HH:mm:ss`), Asia/Jakarta (UTC+07:00).

| Field | Type / Unit | Description |
|---|---|---|
| timestamp | datetime | Local observation time |
| cctv_id | string | Camera id (e.g., cctv1) |
| car, motorcycle, bus, truck | int | Per-snapshot counts (ROI) |
| total_vehicles | int | Sum of classes |
| temp_c | float (°C) | Hourly temperature |
| humidity_pct | float (%) | Hourly relative humidity |
| wind_ms | float (m/s) | Hourly wind speed |
| queue_count | int | Vehicles inside ROI |
| queue_length_meters | int (m) | Queue length (px→meter) |
| queue_status | string (`ok`/`blocked`) | STOP-ZONE status |
