import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race):

    url = f"https://www.boatrace.jp/owpc/pc/race/odds3t?rno={race}&jcd={place:02d}&hd=20260705"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    print("STATUS:", html.status_code)
    print("URL:", html.url)
    print("CONTENT-TYPE:", html.headers.get("content-type"))
    print(html.text[:1000])

    soup = BeautifulSoup(html.text, "html.parser")
    print("TITLE:", soup.title)

    return pd.DataFrame(
    [[
        str(soup.title),
        len(soup.select("table"))
    ]],
    columns=["買い目", "オッズ"]
)
