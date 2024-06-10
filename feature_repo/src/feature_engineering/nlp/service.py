import os
from gensim import matutils
from pyvi import ViTokenizer
import string
import re
import numpy as np
import regex as re
import math
from constant import Char

uniChars = Char.UNICHARS
unsignChars = Char.UNSIGNCHARS
PUNCT_TO_REMOVE = string.punctuation

vowel_table = Char.VOWEL_TABLE
first_char_table = Char.FIRST_CHAR_TABLE
vowel_to_ids = {}


def loaddicchar():
    dic = {}
    char1252 = Char.CHAR1252.split(
        '|')
    charutf8 = Char.CHARUTF8.split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic


dicchar = loaddicchar()


def gen_text(object):
    res = []
    if object['detailed_address'] == object['detailed_address']:
        text = f"Bán nhà tại {object['detailed_address']}"
        res.append(text)
    if math.isnan(object['number_of_floors']):
        res.append(f"Xây {object['number_of_floors']} tầng")
        res.append(f"{object['number_of_floors']}t")
        res.append(f"Thiết kế xây {object['number_of_floors']}t")
        res.append(f"Thiết kế xây {object['number_of_floors']} tầng")

    if math.isnan(object['acreage']):
        res.append(f"Diện tích {object['acreage']}m²")
        res.append(f"{object['acreage']}m²")
        if object['detailed_address'] == object['detailed_address']:
            res.append(
                f"Bán nhà tại {object['detailed_address']}, {object['acreage']}m")

    if math.isnan(object['facede']):
        res.append(f"{object['facede']}M MT")

    if math.isnan(object['number_of_bedrooms']):
        res.append(f"Nhà có {object['facede']} phòng ngủ")
        res.append(f"{object['facede']} phòng ngủ")

    if math.isnan(object['is_car_road']):
        if object['is_car_road'] == 0:
            res.append(
                f"Nhà cách ngõ ô tô tránh {object['cach_ngo_o_to_tranh']}m")
            res.append(
                f"Cách {object['cach_ngo_o_to_tranh']}m ra ngõ ô tô tránh")
            res.append(
                f"Cách Mặt Ngõ Ô Tô Tránh {object['cach_ngo_o_to_tranh']}m")
        elif object['is_car_road'] == 1:
            res.append(f"Nhà ở ngay mặt ngõ")
            res.append(f"Nhà ở mặt ngõ")

    res = '. '.join(res)
    res = res.strip()

    return res


for i in range(len(vowel_table)):
    for j in range(len(vowel_table[i]) - 1):
        vowel_to_ids[vowel_table[i][j]] = (i, j)


def standardize_vietnamese_word_sign(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = list(word)
    sentence_sign = 0
    vowel_index = []
    qu_or_gi = False
    for index, char in enumerate(chars):
        x, y = vowel_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            sentence_sign = y
            chars[index] = vowel_table[x][0]
        if not qu_or_gi or index != 1:
            vowel_index.append(index)
    if len(vowel_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = vowel_to_ids.get(chars[1])
                chars[1] = vowel_table[x][sentence_sign]
            else:
                x, y = vowel_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = vowel_table[x][sentence_sign]
                else:
                    chars[1] = vowel_table[5][sentence_sign] if chars[1] == 'i' else vowel_table[9][sentence_sign]
            return ''.join(chars)
        return word

    for index in vowel_index:
        x, y = vowel_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = vowel_table[x][sentence_sign]
            # for index2 in vowel_index:
            #     if index2 != index:
            #         x, y = vowel_to_ids[chars[index]]
            #         chars[index2] = vowel_table[x][0]
            return ''.join(chars)

    if len(vowel_index) == 2:
        if vowel_index[-1] == len(chars) - 1:
            x, y = vowel_to_ids[chars[vowel_index[0]]]
            chars[vowel_index[0]] = vowel_table[x][sentence_sign]
            # x, y = vowel_to_ids[chars[vowel_index[1]]]
            # chars[vowel_index[1]] = vowel_table[x][0]
        else:
            # x, y = vowel_to_ids[chars[vowel_index[0]]]
            # chars[vowel_index[0]] = vowel_table[x][0]
            x, y = vowel_to_ids[chars[vowel_index[1]]]
            chars[vowel_index[1]] = vowel_table[x][sentence_sign]
    else:
        # x, y = vowel_to_ids[chars[vowel_index[0]]]
        # chars[vowel_index[0]] = vowel_table[x][0]
        x, y = vowel_to_ids[chars[vowel_index[1]]]
        chars[vowel_index[1]] = vowel_table[x][sentence_sign]
        # x, y = vowel_to_ids[chars[vowel_index[2]]]
        # chars[vowel_index[2]] = vowel_table[x][0]
    return ''.join(chars)


def is_valid_vietnam_word(word):
    chars = list(word)
    vowel_index = -1
    for index, char in enumerate(chars):
        x, y = vowel_to_ids.get(char, (-1, -1))
        if x != -1:
            if vowel_index == -1:
                vowel_index = index
            else:
                if index - vowel_index != 1:
                    return False
                vowel_index = index
    return True


def standardize_vietnamese_sentence_sign(sentence):

    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)',
                    r'\1/\2/\3', word).split('/')
        # print(cw)
        if len(cw) == 3:
            cw[1] = standardize_vietnamese_word_sign(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)


def covert_unicode(txt):
    return re.sub(
        Char.REGEX_UNICODE_TEMPLATE,
        lambda x: dicchar[x.group()], txt)


def preprocess_text(text):
    try:
        text = text.lower()
        text = covert_unicode(text)
        text = standardize_vietnamese_sentence_sign(text)
        return text
    except:
        return np.nan


def remove_emoji(text):
    emoji_pattern = Char.EMOJI_PATTERN
    return emoji_pattern.sub(r'', text)


def remove_special_character(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
    text = text.replace('\n', '')
    text = text.strip()
    words = text.split(" ")
    words = [word for word in words if word != ""]
    return " ".join(words)


