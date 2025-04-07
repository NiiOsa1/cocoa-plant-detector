# yolo_batch_inference_v2.py
import os
from ultralytics import YOLO
from pathlib import Path

# ✅ Paths
tiles_dir = "/home/nii-osa/Projects/Cocoa_Field/tiles1"
output_dir = "/home/nii-osa/Projects/YOLO8/runs/qgis_output_tiles1"
weights_path = "/home/nii-osa/Projects/YOLO8/runs/cocoa_yolov8s_phase4_refined/weights/best.pt"

# ✅ Load YOLO model
model = YOLO(weights_path)

# 🧩 Run inference on each tile
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
