## Quick start
python -m venv .venv
# Windows: .venv\Scripts\activate   |  Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # lalu isi OPENWEATHER_API_KEY

## Run order
python cs2_snapshot_weather.py
python yolov8_cctv1_queue_length.py
python merge_queue_weather.py
python preprocess_dataset_stage1.py
python preprocess_dataset_stage2.py
