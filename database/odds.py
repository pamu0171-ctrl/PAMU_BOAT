import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race):

    url = f"https://www.boatrace.jp/owpc/pc/race/odds3t?rno={race}&jcd={place:02d}"

    headers = {
        "User-Agent": "Mozilla/5.0"
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
    print(html.text[:1000])

    soup = BeautifulSoup(html.text, "html.parser")
    print("TITLE:", soup.title)

    tables = soup.select("table")
    print("TABLE COUNT:", len(tables))

    for i, table in enumerate(tables):
        print(f"TABLE {i}")
        print(table.get_text()[:500])

    return pd.DataFrame(
        [[
            str(soup.title),
            len(tables)
        ]],
        columns=["買い目", "オッズ"]
    )
