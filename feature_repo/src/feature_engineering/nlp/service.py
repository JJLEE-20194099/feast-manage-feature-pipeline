from app.modules.classify.fileProcess import FileStore, FileReader
from app.modules.classify import settings
import os
from gensim import matutils
from pyvi import ViTokenizer
import string
import re
import numpy as np
import regex as re
import math
from app.utils.constant import Char

uniChars = Char.UNICHARS
unsignChars = Char.UNSIGNCHARS
PUNCT_TO_REMOVE = string.punctuation

vowel_table = Char.VOWEL_TABLE
first_char_table = Char.FIRST_CHAR_TABLE
vowel_to_ids = {}

stopwords = FileReader(settings.STOP_WORDS).read_stopwords()


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


def segmentation(text):
    return ViTokenizer.tokenize(text)


def split_words(text):
    text = segmentation(text)
    try:
        return [x.strip(settings.SPECIAL_CHARACTER).lower() for x in text.split()]
    except TypeError:
        return []

def get_words_feature(text):
    _split_words = split_words(text)
    return [word for word in _split_words if word.encode('utf-8') not in stopwords and word != '']

class FeatureExtraction(object):
    def __init__(self, data):
        self.data = data

    def __build_dictionary(self):
        print('Building dictionary')
        dict_words = []
        i = 0
        for text in self.data:
            i += 1
            print("Dictionary Step {} / {}".format(i, len(self.data)))
            words = get_words_feature(text['content'])
            dict_words.append(words)
        FileStore(filePath=settings.DICTIONARY_PATH).store_dictionary(
            dict_words)

    def __load_dictionary(self):
        if os.path.exists(settings.DICTIONARY_PATH) == False:
            self.__build_dictionary()
        self.dictionary = FileReader(
            settings.DICTIONARY_PATH).load_dictionary()

    def __build_dataset(self):
        print('Building dataset')
        self.features = [self.get_dense(d['content']) for d in data]
        self.labels = [self.get_dense(d['content']) for d in d['category']]

    def get_dense(self, text):
        words = get_words_feature(text)
        # Bag of words
        self.__load_dictionary()
        vec = self.dictionary.doc2bow(words)
        dense = list(matutils.corpus2dense(
            [vec], num_terms=len(self.dictionary)).T[0])
        return dense

    # def build_tfidf(self,text):

    def get_data_and_label_tfidf(self):
        print('Building dataset')
        self.features = [' '.join(get_words_feature(d['content'])) for d in self.data]
        self.labels = [d['category'] for d in self.data]
        return self.features, self.labels

    def get_data_and_label_bow(self):
        self.__build_dataset()
        return self.features, self.labels

    def read_feature(self):
        return self.data['features'], self.data['labels']


def get_feature_dict(value_features, value_labels):
    return {
        "features": value_features,
        "labels": value_labels
    }
