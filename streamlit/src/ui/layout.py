import streamlit as st
from pathlib import Path
from src.services.load_env import load_env


def load_css():
    # Load CSS into session state to eliminate loading
    if "css" not in st.session_state:
        config = load_env()
        STYLE_PATH = config["STYLE_PATH"]
        st.session_state.css = Path(STYLE_PATH).read_text()

    # Inject CSS on each page load
    st.markdown(f"<style>{st.session_state.css}</style>", unsafe_allow_html=True)


def get_home_image_path():
    config = load_env()
    path = config["HOME_IMAGE_PATH"]
    return path
