import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race, date):

    url = f"https://www.boatrace.jp/owpc/pc/race/odds3t?hd={date}&jcd={place:02d}&rno={race}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.36 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.boatrace.jp/",
        "Connection": "keep-alive"
    }

    html = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("STATUS:", html.status_code)
    print("URL:", html.url)
    print("FINAL URL:", url)
    print("CONTENT-TYPE:", html.headers.get("content-type"))
    print(html.text[:5000])

    soup = BeautifulSoup(html.text, "html.parser")
    print("TITLE:", soup.title)

    tables = soup.select("table")
    print("TABLE COUNT:", len(tables))

    for i, table in enumerate(tables):
        print(f"TABLE {i}")
        print(table.get_text()[:500])

    rows = []

    for table in tables:
        for tr in table.select("tr"):
            cols = [td.get_text(" ", strip=True) for td in tr.select("td")]

            if len(cols) >= 2:
                rows.append(cols[:2])

    return pd.DataFrame(
        rows,
        columns=["買い目", "オッズ"]
    )
