# AI Profile Picture Maker MVP using Streamlit + Replicate API (Text-to-Image Only)

import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO
import replicate

# --- CONFIG ---
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

MODEL = "stability-ai/stable-diffusion"
VERSION = "db21e45a53c0cfa2764dfd2459447f43f6040b3d0d4efdf631dfb7aa15268f94"

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
st.markdown("Choose a theme to generate a fresh AI-stylized profile picture. No upload needed!")

# Themes (prompts)
themes = {
    "Professional": "professional portrait, studio lighting, corporate headshot",
    "Casual": "natural lighting casual portrait of a friendly person",
    "Dating / Soft Glam": "romantic soft glam portrait, beautiful lighting",
    "Anime Style": "anime style headshot, vibrant colors",
    "Fantasy Art": "fantasy elf portrait, digital art"
}

selected_theme = st.selectbox("Choose a style:", list(themes.keys()))

if st.button("Generate My AI-Styled Pic"):
    with st.spinner("Generating your AI profile picture..."):
        try:
            prompt = themes[selected_theme]
            output = replicate.run(
                f"{MODEL}:{VERSION}",
                input={"prompt": prompt, "width": 512, "height": 512}
            )
            if isinstance(output, list):
                result_url = output[0]
            else:
                result_url = output

            result_img = Image.open(BytesIO(requests.get(result_url).content))
            st.success(f"Here is your {selected_theme} style profile picture!")
            st.image(result_img, caption=f"{selected_theme} Style", use_container_width=True)
            st.download_button("Download Image", data=requests.get(result_url).content, file_name="styled_profile_pic.jpg")
        except Exception as e:
            st.error(f"Failed to generate image: {e}")

st.markdown("---")
st.caption("Powered by AI. Try different styles to explore your look!")
