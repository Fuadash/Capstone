import streamlit as st
from pathlib import Path


def load_css():
    css = Path("assets/styles.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
