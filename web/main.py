import os
import sys
import re
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

from database.query import get_ai, get_odds_table

st.set_page_config(
    page_title="PAMU BOAT",
    page_icon="🚤",
    layout="wide"
)

PLACE_NAMES = {
    1: "桐生",
    2: "戸田",
    3: "江戸川",
    4: "平和島",
    5: "多摩川",
    6: "浜名湖",
    7: "蒲郡",
    8: "常滑",
    9: "津",
    10: "三国",
    11: "びわこ",
    12: "住之江",
    13: "尼崎",
    14: "鳴門",
    15: "丸亀",
    16: "児島",
    17: "宮島",
    18: "徳山",
    19: "下関",
    20: "若松",
    21: "芦屋",
    22: "福岡",
    23: "唐津",
    24: "大村",
}

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


@st.cache_data(ttl=300)
def get_active_places(date):
    url = f"https://www.boatrace.jp/owpc/pc/race/index?hd={date}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.boatrace.jp/"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    place_codes = set()

    for a in soup.select("a[href]"):
        href = a.get("href", "")
        match = re.search(r"jcd=(\d{2})", href)

        if match:
            place_codes.add(int(match.group(1)))

    places = [
        code for code in sorted(place_codes)
        if code in PLACE_NAMES
    ]

    return places


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


def load_ai_safe(place, race, date):
    try:
        df = get_ai(
            place,
            race,
            date
        )
    except Exception as e:
        return pd.DataFrame(), str(e)

    if df is None or df.empty:
        return pd.DataFrame(), "AIデータが空です。"

    required_columns = [
        "枠",
        "選手名",
        "AI確率%"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        return pd.DataFrame(), f"AIデータの列が不足しています：{', '.join(missing_columns)}"

    return df, ""


def load_odds_safe(place, race, date):
    try:
        odds = get_odds_table(
            place,
            race,
            date
        )
    except Exception as e:
        return pd.DataFrame(), str(e)

    if odds is None or odds.empty:
        return pd.DataFrame(), "オッズデータが空です。"

    required_columns = [
        "買い目",
        "オッズ"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in odds.columns
    ]

    if missing_columns:
        return pd.DataFrame(), f"オッズデータの列が不足しています：{', '.join(missing_columns)}"

    return odds, ""


st.title("🚤 PAMU BOAT β")

today = datetime.now(
    ZoneInfo("Asia/Tokyo")
).strftime("%Y%m%d")

date = st.text_input(
    "開催日（YYYYMMDD）",
    today
)

active_places = get_active_places(date)

if not active_places:
    st.warning("開催場を取得できませんでした。全24場を表示します。")
    active_places = list(PLACE_NAMES.keys())

place_labels = [
    f"{PLACE_NAMES[code]}（{code:02d}）"
    for code in active_places
]

place_map = {
    f"{PLACE_NAMES[code]}（{code:02d}）": code
    for code in active_places
}

place_label = st.selectbox(
    "開催場",
    place_labels
)

place = place_map[place_label]

race = st.number_input(
    "レース",
    1,
    12,
    1
)

st.subheader("AI予想")

df, ai_error = load_ai_safe(
    place,
    race,
    date
)

if ai_error:
    st.info("このレースのAIデータはまだありません。")
    with st.expander("詳細"):
        st.write(ai_error)
else:
    df = df.sort_values(
        "AI確率%",
        ascending=False
    ).reset_index(drop=True)

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

odds, odds_error = load_odds_safe(
    place,
    race,
    date
)

if odds_error:
    st.warning("オッズを取得できませんでした。")
    with st.expander("詳細"):
        st.write(odds_error)
    st.stop()

odds = odds[
    odds["買い目"].str.startswith(f"{head}-")
].copy()

if odds.empty:
    st.info("この1着固定のオッズはありません。")
    st.stop()

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

