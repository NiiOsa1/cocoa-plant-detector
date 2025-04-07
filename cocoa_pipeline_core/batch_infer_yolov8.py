import os
from ultralytics import YOLO
from pathlib import Path
import requests

# ✅ Model config
MODEL_URL = "https://drive.google.com/uc?export=download&id=1-YJ9n4eoUO-JBcg4BYBmbogrA56F-9FN"
MODEL_PATH = "runs/cocoa_yolov8s_phase4_refined/weights/best.pt"

# ✅ Tile & output folders
tiles_dir = "test_data"  # Change this to real tiles if needed
output_dir = "runs/custom_output"

# ✅ Auto-download model if missing
def download_model_if_missing():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print("📥 Model not found. Downloading from Google Drive...")
        try:
            response = requests.get(MODEL_URL)
            response.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            print("✅ Model downloaded successfully.")
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            exit(1)

download_model_if_missing()

# ✅ Load model
model = YOLO(MODEL_PATH)

# 🧩 Run inference
tile_files = sorted(Path(tiles_dir).glob("*.tif"))
print(f"🧩 Found {len(tile_files)} tiles.")

for tile_path in tile_files:
    print(f"🔍 Predicting: {tile_path.name}")
    model.predict(
        source=str(tile_path),
        conf=0.22,
        iou=0.73,
        save=True,
        save_txt=True,
        save_conf=True,
        project=output_dir,
        name="detections1",
        exist_ok=True
    )

print("✅ YOLO batch inference complete.")
