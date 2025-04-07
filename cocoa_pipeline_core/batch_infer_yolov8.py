# cocoa_pipeline_core/batch_infer_yolov8.py

import os
import argparse
from ultralytics import YOLO
from pathlib import Path
import requests

# ✅ Auto-download model if not present
def download_weights_if_needed(path, url):
    if not os.path.exists(path):
        print("📥 Downloading YOLOv8 model from Google Drive...")
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            response = requests.get(url)
            response.raise_for_status()
            with open(path, "wb") as f:
                f.write(response.content)
            print("✅ Model downloaded successfully.")
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            exit(1)

# ✅ Parse CLI args
parser = argparse.ArgumentParser(description="YOLOv8 Batch Inference on Tiled Images")
parser.add_argument("--tiles", required=True, help="Path to folder with tiled .tif images")
parser.add_argument("--output", default="runs/qgis_output", help="Output folder for predictions")
args = parser.parse_args()

# ✅ Paths
tiles_dir = args.tiles
output_dir = args.output
weights_path = "runs/cocoa_yolov8s_phase4_refined/weights/best.pt"
model_url = "https://drive.google.com/uc?export=download&id=1-YJ9n4eoUO-JBcg4BYBmbogrA56F-9FN"

download_weights_if_needed(weights_path, model_url)
model = YOLO(weights_path)

# 🧩 Run inference
tile_files = sorted(Path(tiles_dir).glob("*.tif"))
print(f"🧩 Found {len(tile_files)} tiles in {tiles_dir}")

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
