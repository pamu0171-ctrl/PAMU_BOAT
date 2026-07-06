import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race, date):

    url = (
        f"https://www.boatrace.jp/owpc/pc/race/odds3t"
        f"?hd={date}&jcd={place:02d}&rno={race}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.boatrace.jp/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    soup = BeautifulSoup(response.text, "html.parser")

    rows = []

    for table in soup.select("table"):
        for tr in table.select("tr"):

            cols = [
                td.get_text(" ", strip=True)
                for td in tr.select("td")
            ]

            if len(cols) >= 2:
                rows.append(cols[:2])

    return pd.DataFrame(
        rows,
        columns=["買い目", "オッズ"]
    )
