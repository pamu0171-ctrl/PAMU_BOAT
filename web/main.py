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

BOAT_COLORS = {
    1: "#ffffff",
    2: "#222222",
    3: "#e94b5b",
    4: "#3f8df5",
    5: "#f4e34f",
    6: "#31b56a",
}

BOAT_TEXT = {
    1: "#111111",
    2: "#ffffff",
    3: "#ffffff",
    4: "#ffffff",
    5: "#111111",
    6: "#ffffff",
}


def boat_badge(num):
    bg = BOAT_COLORS[num]
    fg = BOAT_TEXT[num]
    return (
        f"<span style='display:inline-block;min-width:28px;"
        f"padding:4px 8px;border-radius:6px;background:{bg};"
        f"color:{fg};font-weight:700;text-align:center;"
        f"border:1px solid #555;'>{num}</span>"
    )


def make_matrix_html(matrix, head):
    html = """
    <style>
    .odds-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 6px;
        font-size: 18px;
    }
    .odds-table th {
        text-align: center;
        padding: 6px;
    }
    .odds-table td {
        text-align: center;
        padding: 10px 6px;
        border-radius: 8px;
        background: #1f232b;
        border: 1px solid #333844;
        min-width: 58px;
    }
    .odds-empty {
        background: transparent !important;
        border: none !important;
    }
    .odds-value {
        font-weight: 700;
        font-size: 18px;
    }
    </style>
    """

    html += "<div style='margin-bottom:10px;'>"
    html += f"<b>1着固定：</b> {boat_badge(head)}"
    html += "</div>"

    html += "<table class='odds-table'>"
    html += "<tr><th>3着＼2着</th>"

    for col in matrix.columns:
        html += f"<th>{boat_badge(int(col))}</th>"

    html += "</tr>"

    for idx, row in matrix.iterrows():
        html += f"<tr><th>{boat_badge(int(idx))}</th>"

        for val in row:
            if val == "":
                html += "<td class='odds-empty'></td>"
            else:
                html += f"<td><span class='odds-value'>{val}</span></td>"

        html += "</tr>"

    html += "</table>"
    return html


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

mode = st.radio(
    "表示方法",
    ["公式風", "一覧", "マトリクス"],
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

    if mode == "マトリクス":
        st.write("行 = 3着　　列 = 2着")
        st.dataframe(
            matrix,
            use_container_width=True
        )
    else:
        st.markdown(
            make_matrix_html(matrix, head),
            unsafe_allow_html=True
        )
