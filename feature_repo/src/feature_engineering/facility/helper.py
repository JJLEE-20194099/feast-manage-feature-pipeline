import math
from typing import Union, List
import numpy as np
import pickle
import json

from src.feature_engineering.facility.constant import Distance

Num = Union[int, float]

class IOReader(object):
    def __init__(self, type_of_file: str, path: str):
        self.type_of_file = type_of_file
        self.path = path

    def read(self):
        if self.type_of_file in ['pk', 'pkl']:
            pkl_file = open(self.path, 'rb')
            label_encoder = pickle.load(pkl_file)
            pkl_file.close()
            return label_encoder

        return json.load(open(self.path, encoding='utf-8'))

    def read_by_key(self, key: str):
        return self.read()[key]

def distance_func(lat1: float, lon1: float, lat2: float, lon2: float):

    try:
        R = Distance.RADIUS
        dLat = (lat2-lat1) * math.pi / 180
        dLon = (lon2-lon1) * math.pi / 180
        lat1 = lat1 * math.pi / 180
        lat2 = lat2 * math.pi / 180
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * \
            math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d*1000
    except: # pylint: disable=bare-except
        print(f"Distance_Func error with: {(lat1, lon1, lat2, lon2)}")


def cal_distance(lat1_list: List[Num], lon1_list: List[Num], lat2_list: List[Num], lon2_list: List[Num]):
    try:
        all_res = []
        for i, lat2 in enumerate(lat2_list):
            lon2 = lon2_list[i]
            each_location_res = []
            for j, lat1 in enumerate(lat1_list):
                lon1 = lon1_list[j]
                each_location_res.append(distance_func(lat1, lon1, lat2, lon2))
            all_res.append(each_location_res)

        return all_res
    except: # pylint: disable=bare-except
        print(
            f"cal_distance error with: {(lat1_list, lon1_list, lat2_list, lon2_list)}")


def far_or_not(x: float, distance: float):
    try:
        if x > distance:
            return distance * Distance.MULTIPLE_TRANSFORM_COEFF
        return x / distance
    except: # pylint: disable=bare-except
        print(f"far_or_not with: {(x, distance)}")


def far_or_not_by_list(distance_input_arr, distance):
    try:
        all_res = []
        for instance in distance_input_arr:
            each_res = []
            for dis_candidate in instance:
                each_res.append(far_or_not(dis_candidate, distance))
            all_res.append(each_res)
        return all_res
    except: # pylint: disable=bare-except
        print(f"far_or_not_by_list with: {(distance_input_arr, distance)}")


def preprocess_distance(distance):
    if distance > Distance.MULTIPLE_TRANSFORM_COEFF:
        return np.nan
    return distance
