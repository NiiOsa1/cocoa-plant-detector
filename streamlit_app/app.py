import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import tempfile
import requests

# ✅ Google Drive model download config
MODEL_URL = "https://drive.google.com/uc?export=download&id=1-YJ9n4eoUO-JBcg4BYBmbogrA56F-9FN"
MODEL_PATH = "best.pt"

# ✅ Download model if not present
def download_model():
    if not os.path.exists(MODEL_PATH):
        st.warning("📥 Downloading YOLOv8 model from Google Drive...")
        try:
            response = requests.get(MODEL_URL)
            response.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            st.success("✅ Model downloaded successfully.")
        except Exception as e:
            st.error(f"❌ Failed to download model: {e}")

# 📥 Trigger download
download_model()

# ✅ Set up Streamlit app
st.set_page_config(page_title="Cocoa Plant + Hole Detector", layout="centered")

st.markdown("## 🧠 Cocoa Plant + Hole Detector")
st.markdown("Upload a single image tile from your field dataset and run YOLOv8 detection live.")

uploaded_file = st.file_uploader("📁 Upload tile (.tif)", type=["tif", "tiff", "jpg", "jpeg", "png"])

if uploaded_file:
    st.success(f"📥 Image uploaded: {uploaded_file.name}")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_image_path = tmp_file.name

    if st.button("🚀 Run Detection"):
        with st.spinner("Running YOLOv8 detection..."):
            try:
                model = YOLO(MODEL_PATH)
                results = model.predict(source=tmp_image_path, conf=0.05, iou=0.73, save=False)
                annotated = results[0].plot()
                st.image(annotated, caption="✅ Detected: Cocoa Plants + Holes", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Inference failed: {e}")

        os.remove(tmp_image_path)

st.markdown("---")
st.markdown("⚙️ Powered by YOLOv8 + Streamlit | Built by **Michael Ofeor**")
