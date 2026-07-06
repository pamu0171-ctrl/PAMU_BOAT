import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race, date):

    url = (
        f"https://www.boatrace.jp/owpc/pc/race/odds3t"
        f"?hd={date}&jcd={place:02d}&rno={race}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.boatrace.jp/"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    soup = BeautifulSoup(response.text, "html.parser")

    odds_cells = soup.select("td.oddsPoint")
    odds_values = [
        cell.get_text(strip=True)
        for cell in odds_cells
    ]

    rows = []

    if len(odds_values) < 120:
        return pd.DataFrame(
            [[
                "取得失敗",
                f"oddsPoint数: {len(odds_values)}"
            ]],
            columns=["買い目", "オッズ"]
        )

    for first in range(1, 7):
        row_index = 0

        for second in range(1, 7):
            if second == first:
                continue

            for third in range(1, 7):
                if third == first or third == second:
                    continue

                odds_index = row_index * 6 + (first - 1)

                rows.append([
                    f"{first}-{second}-{third}",
                    odds_values[odds_index]
                ])

                row_index += 1

    return pd.DataFrame(
        rows,
        columns=["買い目", "オッズ"]
    )
