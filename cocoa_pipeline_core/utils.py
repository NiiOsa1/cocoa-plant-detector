import os
import requests

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
