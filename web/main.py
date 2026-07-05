
import os
import sys

# sys.path.append("/content")
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)
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
df = get_ai(place, race)

st.write(f"◎ 本命：{df.iloc[0]['枠']}号艇 {df.iloc[0]['選手名']}")

st.dataframe(df, use_container_width=True, hide_index=True)

