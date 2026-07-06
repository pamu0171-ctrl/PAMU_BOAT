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

    rows = []

    for table in soup.select("table"):

        for tr in table.select("tr"):

            tds = tr.select("td")

            if len(tds) < 2:
                continue

            cols = [
                td.get_text(" ", strip=True)
                for td in tds
            ]

            rows.append([
                cols[0],
                cols[1]
            ])

    return pd.DataFrame(
        rows,
        columns=["買い目", "オッズ"]
    )
