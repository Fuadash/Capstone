import streamlit as st
from src.services.data_loader import load_data
from src.ui.filters import render_sidebar_filters
from src.utils.filtering import apply_filters
from src.ui.charts import releases_per_year, avg_price_per_year, price_distribution, rating_distribution, score_by_genre
from src.services.load_env import load_env

st.title("Trends")

# hacky solution
for key, val in st.session_state.items():
    if (key == "selected_game_name" or key == "selected_appid" or key=="search_text"):
        st.session_state[key] = val


config = load_env()
DATA_PATH = config["DATA_PATH"]
df = load_data(DATA_PATH)
filters = render_sidebar_filters(df)
filtered = apply_filters(df, filters)


def render_chart(chart, data):
    if not data.empty:
        return st.plotly_chart(chart(data), use_container_width=True)
    else:
        return st.warning("No Games to Display")


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Releases", "Avg Price", "Price Dist.", "Rating Dist.", "Score by Genre"])
with tab1:
    render_chart(releases_per_year, filtered)
with tab2:
    render_chart(avg_price_per_year, filtered)
with tab3:
    render_chart(price_distribution, filtered)
with tab4:
    render_chart(rating_distribution, filtered)
with tab5:
    render_chart(score_by_genre, filtered)
