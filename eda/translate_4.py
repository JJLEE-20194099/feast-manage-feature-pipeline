import pandas as pd
import numpy as np
import requests
from tqdm import tqdm


df = pd.read_csv('../data/process_v1/process_data_5.csv')

lst_proxy = []
with open(r"../data/ip.txt", 'r') as f:
    for line in f:
        lst_proxy.append(line.strip())


def translate_gg_free(text, tgt_lang = "en", src_lang = "vi"):
    txt = str(text)
    proxies = {
        "http": lst_proxy
    }
    tran = ''
    try:
        r = requests.get(
            'https://translate.googleapis.com/translate_a/single?client=gtx&sl=' + src_lang + '&tl=' + tgt_lang +
            '&dt=t&dt=bd&dj=1&q=' + txt, proxies=proxies)
        if r.status_code == 200:
            resp = r.json()
            for j in resp['sentences']:
                tran += j['trans'] + " "
    except Exception as ve:
        print(ve)
    return tran

descs = df['description'].tolist()
eng_descs = []
for i, desc in tqdm(enumerate(descs[60000:80000])):
    try:
        en_desc = translate_gg_free(desc)
        eng_descs.append(en_desc)
    except Exception as e:
        print(e)
        eng_descs.append(np.nan)

    if (i + 1) % 1000 == 0:
        eng_df = pd.DataFrame()
        eng_df['en_description'] = eng_descs
        eng_df['description'] = descs[:i + 1]
        eng_df.to_csv(f'../data/process_v1/trans/eng_4_{i + 1}.csv', index = False)
