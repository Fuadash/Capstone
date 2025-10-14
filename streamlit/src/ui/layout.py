import streamlit as st
from pathlib import Path
from src.services.load_env import load_env


def load_css():
    config = load_env()
    STYLE_PATH = config["STYLE_PATH"]
    css = Path(STYLE_PATH).read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def get_home_image_path():
    config = load_env()
    path = config["HOME_IMAGE_PATH"]
    return path
