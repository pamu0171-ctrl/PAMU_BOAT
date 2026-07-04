
import pandas as pd

from PAMU_BOAT.database.query import get_race


def ai_report(place, race):

    df = get_race(place, race)

    df = df.copy()

    df["AI順位"] = (
        df["AI確率%"]
        .rank(ascending=False, method="min")
        .astype(int)
    )

    return df[
        [
            "AI順位",
            "枠",
            "選手名",
            "着",
            "AI確率%",
            "AI評価"
        ]
    ]
