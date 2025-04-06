import argparse
from cocoa_cli_pipeline import tiler, infer, geoconvert

def main():
    parser = argparse.ArgumentParser(description="🧠 Cocoa Detection CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # 🧱 Tile command
    tile_parser = subparsers.add_parser("tile", help="Tile large aerial image")
    tile_parser.add_argument("--input", required=True, help="Path to large .tif image")
    tile_parser.add_argument("--output", required=True, help="Folder to save tiles")
    tile_parser.add_argument("--tile-size", type=int, default=1024)
    tile_parser.add_argument("--stride", type=int, default=800)

    # 🧠 Inference command
    infer_parser = subparsers.add_parser("infer", help="Run YOLOv8 batch inference")
    infer_parser.add_argument("--tiles", required=True, help="Path to tiles folder")
    infer_parser.add_argument("--weights", required=True, help="Path to model weights (.pt)")
    infer_parser.add_argument("--output", required=True, help="Output folder for predictions")

    # 🌍 Geoconvert command
    geo_parser = subparsers.add_parser("geoconvert", help="Convert YOLO labels to deduplicated GeoJSON")
    geo_parser.add_argument("--labels", required=True, help="Path to YOLO label .txt files")
    geo_parser.add_argument("--output", required=True, help="Path to save GeoJSON file")
    geo_parser.add_argument("--origin_x", type=float, required=True)
    geo_parser.add_argument("--origin_y", type=float, required=True)
    geo_parser.add_argument("--pixel_width", type=float, required=True)
    geo_parser.add_argument("--pixel_height", type=float, required=True)
    geo_parser.add_argument("--tile_size", type=int, default=1024)
    geo_parser.add_argument("--conf_thresh", type=float, default=0.22)

    args = parser.parse_args()

    if args.command == "tile":
        tiler.run(args.input, args.output, args.tile_size, args.stride)

    elif args.command == "infer":
        infer.run(args.tiles, args.output, args.weights)

    elif args.command == "geoconvert":
        geoconvert.run(
            labels_dir=args.labels,
            output=args.output,
            origin_x=args.origin_x,
            origin_y=args.origin_y,
            pixel_width=args.pixel_width,
            pixel_height=args.pixel_height,
            tile_size=args.tile_size,
            conf_thresh=args.conf_thresh
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
