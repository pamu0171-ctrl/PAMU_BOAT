
import pandas as pd

from database.db import connect
from database.odds import get_odds


def get_odds_table(place, race, date):

    conn = connect()

    df = pd.read_sql(
        f"""
        SELECT *
        FROM race_data
        WHERE 場コード={place}
        AND レース={race}
        """,
        conn
    )

    conn.close()

    df = df.sort_values(
        "AI確率%",
        ascending=False
    )

    return df


def get_today():

    conn = connect()

    df = pd.read_sql(
        """
        SELECT DISTINCT
            場コード,
            レース
        FROM race_data
        ORDER BY 場コード, レース
        """,
        conn
    )

    conn.close()

    return df


def get_ai(place, race, date):

    df = get_race(place, race)

    return df[
        [
            "枠",
            "選手名",
            "級別",
            "AI確率%",
            "AI評価"
        ]
    ]
