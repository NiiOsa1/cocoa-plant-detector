# 🧠 Converts YOLO labels to map coordinates, filters by confidence, removes duplicates
# 📍 For Image_4.tif with known georeference
# 🗂️ Based on: tiles in /qgis_output_tiles1/detections1/labels

import os
import json
import glob
from shapely.geometry import Point
from shapely.strtree import STRtree

# 📁 Input paths
labels_dir = "/home/nii-osa/Projects/YOLO8/runs/qgis_output_tiles1/detections1/labels"
output_geojson = "/home/nii-osa/Projects/YOLO8/qgis_ready6_detections.geojson"

# 🎯 Classes
classes = {0: "cocoa-plant", 1: "hole"}

# 🌐 GeoTransform from Image_4.tif metadata
origin_x = 525765.6597444439539686
origin_y = 8702143.3199874181300402
pixel_width = 0.01298099167173574417
pixel_height = -0.01298099167173707123  # North-up image
tile_size = 1024

# 🎚️ Confidence threshold
CONF_THRESHOLD = 0.22

# 🔁 Loop through all label .txt files
features = []
point_geoms = []  # For deduplication
existing = []

label_files = glob.glob(os.path.join(labels_dir, "*.txt"))
print(f"📂 Found {len(label_files)} label files...")

for label_path in label_files:
    filename = os.path.basename(label_path).replace(".txt", "")
    try:
        _, y_str, x_str = filename.split("_")
        tile_x = int(x_str)
        tile_y = int(y_str)
    except ValueError:
        print(f"⚠️ Skipping malformed: {filename}")
        continue

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            cls_id, x, y, w, h = map(float, parts[:5])
            conf = float(parts[5]) if len(parts) == 6 else None

            if conf is not None and conf < CONF_THRESHOLD:
                continue  # ❌ Skip weak detections

            abs_px = tile_x + x * tile_size
            abs_py = tile_y + y * tile_size

            map_x = origin_x + abs_px * pixel_width
            map_y = origin_y + abs_py * pixel_height

            point = Point(map_x, map_y)

            # ✅ Deduplication: check if similar point already added
            is_duplicate = False
            for existing_pt in existing:
                if point.distance(existing_pt) < 0.3:  # < 30cm threshold
                    is_duplicate = True
                    break
            if is_duplicate:
                continue

            existing.append(point)  # Track added points

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [map_x, map_y]
                },
                "properties": {
                    "class": classes.get(int(cls_id), f"class_{cls_id}"),
                    "confidence": conf
                }
            }
            features.append(feature)

# 📦 Export GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open(output_geojson, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"\n✅ Final cleaned GeoJSON exported with {len(features)} deduplicated detections")
print(f"→ {output_geojson}")
