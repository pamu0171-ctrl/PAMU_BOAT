import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race):

    url = "https://www.boatrace.jp/owpc/pc/race/odds3t?rno={race}&jcd={place:02d}"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Referer": "https://www.boatrace.jp/",
    "Connection": "keep-alive"
}

    session = requests.Session()

session.headers.update(headers)

session.get("https://www.boatrace.jp")

html = session.get(
    url,
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
