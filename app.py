# AI Profile Picture Maker MVP using Streamlit + Replicate API

import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO

# --- CONFIG ---
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Set this in your local environment or Streamlit Cloud
MODEL_VERSION = "tencentarc/stylegan3"

# --- UI ---
st.set_page_config(page_title="AI Profile Picture Maker", layout="centered")
st.title("🎨 AI Profile Picture Maker")
st.markdown("Upload a selfie and get amazing themed profile pictures!")

# Theme selector
themes = ["Professional", "Casual", "Dating", "Anime", "Fantasy"]
selected_theme = st.selectbox("Choose a style:", themes)

# File upload
uploaded_file = st.file_uploader("Upload a clear selfie (JPG/PNG)", type=["jpg", "jpeg", "png"])

# --- FUNCTION TO CALL REPLICATE API ---
def generate_image_with_replicate(image_bytes, theme):
    url = f"https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    # For demonstration, this is a placeholder payload. Customize based on the chosen model.
    payload = {
        "version": MODEL_VERSION,
        "input": {
            "image": "data:image/jpeg;base64," + image_bytes.encode("base64"),
            "style": theme.lower()
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# --- PROCESSING ---
if uploaded_file:
    st.image(uploaded_file, caption="Original Selfie", width=300)
    if st.button("Generate My AI Profile Pic"):
        with st.spinner("Generating... this may take 20-40 seconds"):
            # Simulate API call - replace this with real Replicate API later
            try:
                img = Image.open(uploaded_file).convert("RGB")
                st.success("Your AI profile picture is ready!")
                st.image(img, caption=f"{selected_theme} Style (sample)", width=300)
                st.download_button("Download Image", data=uploaded_file.getvalue(), file_name="ai_profile_pic.jpg")
            except Exception as e:
                st.error(f"Failed to generate image: {e}")

st.markdown("---")
st.caption("This is a demo version. Final version will include real AI generation and HD output.")
