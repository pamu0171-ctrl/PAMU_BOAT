import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import pandas as pd
import streamlit as st

from database.query import get_ai, get_odds_table

st.set_page_config(
    page_title="PAMU BOAT",
    page_icon="🚤",
    layout="wide"
)

st.title("🚤 PAMU BOAT β")

place = st.number_input("場コード", 1, 24, 1)

race = st.number_input("レース", 1, 12, 1)

date = st.text_input(
    "開催日（YYYYMMDD）",
    "20260705"
)

st.subheader("AI予想")

df = get_ai(place, race, date)

ai_diff = df.iloc[0]["AI確率%"] - df.iloc[1]["AI確率%"]

if ai_diff >= 20:
    danger = "★☆☆☆☆"
    comment = "イン信頼度 高"
elif ai_diff >= 10:
    danger = "★★★☆☆"
    comment = "被弾注意"
else:
    danger = "★★★★★"
    comment = "被弾妙味あり"

st.write(
    f"◎ 本命：{df.iloc[0]['枠']}号艇 {df.iloc[0]['選手名']}"
)

st.write("🎯 推奨買い目")

st.write(
    f"{df.iloc[0]['枠']}-{df.iloc[1]['枠']}-{df.iloc[2]['枠']}"
)

st.write(
    f"{df.iloc[0]['枠']}-{df.iloc[2]['枠']}-{df.iloc[1]['枠']}"
)

st.write(
    f"{df.iloc[1]['枠']}-{df.iloc[0]['枠']}-{df.iloc[2]['枠']}"
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.subheader("🚨 被弾レーダー")

st.write(f"危険度：{danger}")
st.write(comment)

st.subheader("📊 オッズ")

head = st.radio(
    "1着固定",
    [1, 2, 3, 4, 5, 6],
    horizontal=True
)

odds = get_odds_table(
    place,
    race,
    date
)

odds = odds[
    odds["買い目"].str.startswith(f"{head}-")
].copy()

# ---------------------------------
# 一覧表示 / マトリクス表示
# ---------------------------------

mode = st.radio(
    "表示方法",
    ["一覧", "マトリクス"],
    horizontal=True
)

if mode == "一覧":

    st.dataframe(
        odds,
        use_container_width=True,
        hide_index=True
    )

else:

    boats = [1, 2, 3, 4, 5, 6]
    boats.remove(head)

    matrix = pd.DataFrame(
        "",
        index=boats,
        columns=boats
    )

    for _, row in odds.iterrows():

        first, second, third = map(
            int,
            row["買い目"].split("-")
        )

        matrix.loc[
            third,
            second
        ] = row["オッズ"]

    st.write("行 = 3着　　列 = 2着")

    st.dataframe(
        matrix,
        use_container_width=True
    )
