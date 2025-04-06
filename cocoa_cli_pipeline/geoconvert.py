import os
import json
import glob
import argparse
from shapely.geometry import Point

def run(labels_dir, output, origin_x, origin_y, pixel_width, pixel_height, tile_size, conf_thresh=0.22):
    classes = {0: "cocoa-plant", 1: "hole"}
    features, existing = [], []

    label_files = glob.glob(os.path.join(labels_dir, "*.txt"))
    print(f"📂 Found {len(label_files)} label files...")

    for label_path in label_files:
        filename = os.path.basename(label_path).replace(".txt", "")
        try:
            _, y_str, x_str = filename.split("_")
            tile_x = int(x_str)
            tile_y = int(y_str)
        except ValueError:
            print(f"⚠️ Skipping malformed filename: {filename}")
            continue

        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue

                cls_id, x, y, w, h = map(float, parts[:5])
                conf = float(parts[5]) if len(parts) == 6 else None
                if conf is not None and conf < conf_thresh:
                    continue

                abs_px = tile_x + x * tile_size
                abs_py = tile_y + y * tile_size
                map_x = origin_x + abs_px * pixel_width
                map_y = origin_y + abs_py * pixel_height
                point = Point(map_x, map_y)

                if any(point.distance(p) < 0.3 for p in existing):
                    continue

                existing.append(point)
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [map_x, map_y]},
                    "properties": {
                        "class": classes.get(int(cls_id), f"class_{cls_id}"),
                        "confidence": conf
                    }
                })

    geojson = {"type": "FeatureCollection", "features": features}
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w") as f:
        json.dump(geojson, f, indent=2)

    print(f"✅ Exported {len(features)} cleaned detections → {output}")
