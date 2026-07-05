import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_odds(place, race):

    url = f"https://www.boatrace.jp/owpc/pc/race/odds3t?rno={race}&jcd={place:02d}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers)

    print(html.status_code)

    return pd.DataFrame(
        [["接続成功", html.status_code]],
        columns=["買い目", "オッズ"]
    )
