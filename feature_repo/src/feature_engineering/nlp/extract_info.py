juridical_dict = {
    "Sổ hồng": 0,
    "Sổ đỏ": 1,
    "Hợp đồng mua bán": 2,
    "Giấy tờ hợp lệ": 3,
    "Không xác định": 4,
    "Giấy tờ viết tay": 5
}
def extract_juridical(juridical):
    return juridical_dict[juridical]

def get_juridical(df, source_col, dest_col):
    df[dest_col] = df[source_col].apply(extract_juridical)
    return df[dest_col]


def extract_w_h(area):
    try:
        wh = area.split(" ")[-1]
        wh = wh.replace("(", "")
        wh = wh.replace(")", "")
        w = wh.split("x")[0]
        w = w.replace(',', '.')
        h = wh.split("x")[1]
        h = h.replace(',', '.')
        return float(w), float(h)
    except:
        return None, None

def get_wh(df, source_col, w_col, h_col):
    wh_list = df[source_col].apply(extract_w_h)
    df[w_col] = [wh[0] for wh in wh_list]
    df[h_col] = [wh[1] for wh in wh_list]

    return df[w_col], df[h_col]

