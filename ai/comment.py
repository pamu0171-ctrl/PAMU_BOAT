
def make_comment(row):

    comments = []

    if row["AI確率%"] >= 50:
        comments.append("◎ 本命")

    elif row["AI確率%"] >= 25:
        comments.append("○ 有力")

    elif row["AI確率%"] >= 10:
        comments.append("△ 穴候補")

    if row["枠"] == 1:
        comments.append("イン戦")

    if row["展示順位"] == 1:
        comments.append("展示最速")

    if row["モーター順位"] <= 2:
        comments.append("モーター上位")

    if row["全国勝率順位"] <= 2:
        comments.append("全国勝率上位")

    return " / ".join(comments)
