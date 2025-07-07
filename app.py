# AI Profile Picture Maker MVP using Streamlit + Hugging Face (Free Alternative to Replicate)

import streamlit as st
import requests
import os
import base64
from PIL import Image
from io import BytesIO
from streamlit_image_comparison import image_comparison

# --- UI CONFIG ---
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

# Themes (prompts)
themes = {
    "Professional": "professional portrait, studio lighting",
    "Casual": "natural lighting casual photo",
    "Dating / Soft Glam": "romantic soft glam portrait",
    "Anime Style": "anime style portrait",
    "Fantasy Art": "fantasy elf, digital painting"
}

selected_theme = st.selectbox("Choose a style:", list(themes.keys()))

# File upload
uploaded_file = st.file_uploader("Upload a clear selfie (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Resize and compress image
def preprocess_image(image: Image.Image, max_width=512, quality=85):
    if image.width > max_width:
        new_height = int(max_width * image.height / image.width)
        image = image.resize((max_width, new_height))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return buffer.read()

# Convert to base64 string
def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

# Stylize image using Hugging Face inference API (e.g. timbrooks/instruct-pix2pix)
def stylize_image_with_hf(image_bytes, prompt):
    base64_str = encode_image_to_base64(image_bytes)
    response = requests.post(
        "https://hf.space/embed/timbrooks/instruct-pix2pix/api/predict/",
        json={"data": [f"data:image/jpeg;base64,{base64_str}", prompt]}
    )
    response.raise_for_status()
    result_url = response.json()["data"][0]
    return result_url

# Process input
if uploaded_file:
    original_image = Image.open(uploaded_file).convert("RGB")
    st.image(original_image, caption="Original Selfie", use_container_width=True)

    if st.button("Generate My AI-Styled Pic"):
        with st.spinner("Generating your AI-stylized image... this may take 30–60 seconds"):
            try:
                uploaded_file.seek(0)
                image_bytes = preprocess_image(original_image)
                result_url = stylize_image_with_hf(image_bytes, themes[selected_theme])
                result_img = Image.open(BytesIO(requests.get(result_url).content))

                st.success(f"Here is your {selected_theme} style profile picture!")
                st.image(result_img, caption=f"{selected_theme} Style", use_container_width=True)

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
st.caption("Powered by Hugging Face. Try different styles to see what fits your vibe best.")
