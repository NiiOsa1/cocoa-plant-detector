from ultralytics import YOLO
from pathlib import Path
import os

def run(tiles_dir, output_dir, weights_path, conf=0.22, iou=0.73):
    # ✅ Load YOLO model
    model = YOLO(weights_path)

    # 🧩 Gather tiles
    tile_files = sorted(Path(tiles_dir).glob("*.tif"))
    print(f"🧩 Found {len(tile_files)} tiles in: {tiles_dir}")

    for tile_path in tile_files:
        print(f"🔍 Predicting: {tile_path.name}")
        model.predict(
            source=str(tile_path),
            conf=conf,
            iou=iou,
            save=True,
            save_txt=True,
            save_conf=True,
            project=output_dir,
            name="detections1",
            exist_ok=True
        )

    print(f"✅ Inference complete. Results saved to {output_dir}")
