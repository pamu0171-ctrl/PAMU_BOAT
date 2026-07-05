import pandas as pd


def get_odds(place, race):
        data = [
        ["1-2-3", 7.9],
        ["1-2-4", 5.1],
        ["1-2-5", 14.6],
        ["1-2-6", 13.7],
        ["1-3-2", 19.3],
    ]

    return pd.DataFrame(
        data,
        columns=[
            "買い目",
            "オッズ"
        ]
    )
