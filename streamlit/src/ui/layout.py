import streamlit as st
from pathlib import Path
from src.services.load_env import load_env
import streamlit.components.v1 as components


def load_css():
    if "css_loaded" not in st.session_state:
        config = load_env()
        STYLE_PATH = config["STYLE_PATH"]
        css = Path(STYLE_PATH).read_text()
        components.html(f"<style>{css}</style>", height=0)
        st.session_state.css_loaded = True


def get_home_image_path():
    config = load_env()
    path = config["HOME_IMAGE_PATH"]
    return path
