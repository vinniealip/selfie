# AI Profile Picture Maker MVP using Streamlit + Replicate API with Style Themes and Before/After Slider (Dual Model Version)

import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO
import replicate
from streamlit_image_comparison import image_comparison

# --- CONFIG ---
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Set via Streamlit secrets
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Define models
REALISTIC_MODEL = "fofr/anything-style-transfer"
REALISTIC_VERSION = "e226a16a791ba37a07e0a697835fb3cdce7011cc946265c9ef82c78192116c7d"
STYLIZED_MODEL = "lucataco/face-to-style"
STYLIZED_VERSION = "db2c9f8f83ae738df1f69e7f3c68a1227ea0c7384b27081f5c0112f937cb4090"

# --- UI ---
st.set_page_config(page_title="AI Profile Picture Maker", layout="centered")
st.markdown("""
    <style>
        .main {background-color: #f7f9fc;}
        h1 {color: #1a1a1a; font-family: 'Segoe UI', sans-serif; text-align: center;}
        .stButton > button {background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 8px; font-size: 16px;}
        .stDownloadButton > button {background-color: #2196F3; color: white; padding: 10px 20px; border-radius: 8px; font-size: 16px;}
        .stMarkdown {text-align: center; font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎨 AI Profile Picture Maker")
st.markdown("Upload a selfie and choose a theme to get your AI-stylized profile picture!")

# Theme selector with model types
themes = {
    "Professional": {"prompt": "professional portrait", "model": "realistic"},
    "Casual": {"prompt": "natural lighting casual photo", "model": "realistic"},
    "Dating / Soft Glam": {"prompt": "romantic soft glam portrait", "model": "realistic"},
    "Anime Style": {"prompt": "anime", "model": "stylized"},
    "Fantasy Art": {"prompt": "fantasy elf", "model": "stylized"}
}
selected_theme = st.selectbox("Choose a style:", list(themes.keys()))

# File upload
uploaded_file = st.file_uploader("Upload a clear selfie (JPG/PNG)", type=["jpg", "jpeg", "png"])

# --- PROCESSING ---
def stylize_image(image_bytes, theme):
    uploaded_url = replicate.upload(image_bytes)
    prompt = theme["prompt"]

    if theme["model"] == "realistic":
        output = replicate.run(
            f"{REALISTIC_MODEL}:{REALISTIC_VERSION}",
            input={"image": uploaded_url, "prompt": prompt}
        )
    else:
        output = replicate.run(
            f"{STYLIZED_MODEL}:{STYLIZED_VERSION}",
            input={"image": uploaded_url, "style": prompt}
        )
    return output["output"]

if uploaded_file:
    original_image = Image.open(uploaded_file).convert("RGB")
    st.image(original_image, caption="Original Selfie", use_column_width=True)
    if st.button("Generate My AI-Styled Pic"):
        with st.spinner("Generating your AI-stylized image... this may take 30–60 seconds"):
            try:
                image_bytes = uploaded_file.read()
                result_url = stylize_image(image_bytes, themes[selected_theme])

                result_img = Image.open(BytesIO(requests.get(result_url).content))
                st.success(f"Here is your {selected_theme} style profile picture!")
                st.image(result_img, caption=f"{selected_theme} Style", use_column_width=True)

                # Show before/after comparison
                st.markdown("### Before & After")
                image_comparison(
                    img1=original_image,
                    img2=result_img,
                    label1="Before",
                    label2="After"
                )

                st.download_button("Download Image", data=requests.get(result_url).content, file_name="styled_profile_pic.jpg")
            except Exception as e:
                st.error(f"Failed to generate image: {e}")

st.markdown("---")
st.caption("Powered by AI. Try different styles to see what fits your vibe best.")
