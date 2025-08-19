import streamlit as st
import requests


@st.cache_resource
def http_session():
    s = requests.Session()
    return s


def get_live_game_info(appid, cc="us", lang="en"):
    url = "https://store.steampowered.com/api/appdetails"
    try:
        r = http_session().get(
            url, params={"appids": appid, "cc": cc, "lang": lang}, timeout=10
        )
        r.raise_for_status()
        data = r.json().get(str(appid))
        if data and data.get("success"):
            return data["data"]
    except requests.RequestException:
        return None
