import streamlit as st
from src.services.data_loader import load_data
from src.ui.filters import render_sidebar_filters
from src.utils.filtering import apply_filters
from src.ui.charts import releases_per_year, avg_price_per_year, price_distribution

st.title("Trends")

df = load_data("../etl/data/processed/processed_data.csv")
filters = render_sidebar_filters(df)
filtered = apply_filters(df, filters)

tab1, tab2, tab3 = st.tabs(["Releases", "Avg Price", "Price Dist."])
with tab1:
    st.plotly_chart(releases_per_year(filtered), use_container_width=True)
with tab2:
    st.plotly_chart(avg_price_per_year(filtered), use_container_width=True)
with tab3:
    st.plotly_chart(price_distribution(filtered), use_container_width=True)
