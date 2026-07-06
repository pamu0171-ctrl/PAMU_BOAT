import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race, date):

    url = f"https://www.boatrace.jp/owpc/pc/race/odds3t?hd={date}&jcd={place:02d}&rno={race}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.boatrace.jp/"
    }

    html = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    soup = BeautifulSoup(html.text, "html.parser")

    tables = soup.select("table")

    rows = []

    for i, table in enumerate(tables):
        text = table.get_text(" ", strip=True)

        rows.append([
            f"TABLE {i}",
            text[:300]
        ])

    return pd.DataFrame(
        rows,
        columns=["買い目", "オッズ"]
    )
