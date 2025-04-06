from PIL import Image
import os

def run(input_path, output_dir, tile_size=1024, stride=800):
    # 🧱 Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Allow large images
    Image.MAX_IMAGE_PIXELS = None

    # 🖼️ Open image
    image = Image.open(input_path)
    width, height = image.size
    tile_count = 0

    # 🔄 Loop over tiles with overlap
    for top in range(0, height, stride):
        for left in range(0, width, stride):
            right = min(left + tile_size, width)
            bottom = min(top + tile_size, height)
            tile = image.crop((left, top, right, bottom))

            tile_filename = f"tile_{top}_{left}.tif"
            tile.save(os.path.join(output_dir, tile_filename))
            tile_count += 1

    print(f"✅ Saved {tile_count} tiles to {output_dir}")
