
import os
import sys

# sys.path.append("/content")

import streamlit as st

from database.query import get_ai

st.set_page_config(
    page_title="PAMU BOAT",
    page_icon="🚤",
    layout="wide"
)

st.title("🚤 PAMU BOAT β")

place = st.number_input("場コード", 1, 24, 1)

race = st.number_input("レース", 1, 12, 1)

st.subheader("AI予想")

st.dataframe(get_ai(place, race), use_container_width=True)
