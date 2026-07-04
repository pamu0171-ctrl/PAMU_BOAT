
def score_detail(row):

    score = {}

    score["全国勝率"] = round(row["全国勝率"] * 3)

    score["当地勝率"] = round(row["当地勝率"] * 2)

    score["展示"] = round((7.0 - row["展示 タイム"]) * 100)

    score["モーター"] = round(row["モーター2連率"] / 2)

    score["ST"] = round((0.30 - row["平均ST"]) * 100)

    score["枠"] = 20 if row["枠"] == 1 else 0

    return score
