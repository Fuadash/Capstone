import os
import streamlit as st


def load_env():
    ENV = os.getenv("ENV", "dev")

    if ENV == "dev":
        # local secrets.toml
        config = st.secrets["dev"]
    else:
        # streamlit secrets manager
        config = st.secrets

    return config
