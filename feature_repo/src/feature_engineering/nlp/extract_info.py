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