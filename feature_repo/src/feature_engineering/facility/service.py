import json
from typing import Union
from dataclasses import astuple
import asyncio
import requests
import pandas as pd
from helper import distance_func
from helper import IOReader
from dto.location import (
    LocationConfig,
    PlaceInformationConfig,
    LocationListConfig,
    DetailedLocationConfig
)

from constant import OpenstreetMap, FilePath, MeanOfFacility

from tqdm import tqdm

Num = Union[int, float]

def findpublicfacilities(location_config: LocationConfig):

    lat, lon, distance = astuple(location_config)
    overpass_url = f"{OpenstreetMap.MAIN_DOMAIN}{OpenstreetMap.API_PATH}"

    overpass_query = f"""
      [out:json];
      (
      node["amenity"=""](around:{distance},{lat},{lon});
      way["amenity"=""](around:{distance},{lat},{lon});
      rel["amenity"=""](around:{distance},{lat},{lon});
      );
      out center;
      """

    response = requests.get(overpass_url,
                            params={'data': overpass_query}, timeout=60)

    data = response.json()

    return data['elements']


def count_facilities(lat: float, lon: float, distance: int, response = None):
    if response is not None:
        res = response
    else:
        try:
            res = findpublicfacilities(LocationConfig(
                lat = lat,
                lon = lon,
                distance = distance
            ))
        except Exception as e:
            print(e)
            return {}
    facility_dict = {}
    means_of_facility_obj = json.load(open(FilePath.MEAN_OF_FACILITY_DESC, encoding='utf-8'))
    means_of_facility = means_of_facility_obj["means_of_facility_list"]
    for _fa in means_of_facility:
        facility_dict[_fa] = 0

    for place in res:
        try:
            if place['type'] == MeanOfFacility.TOWNHALL or place['type'] == MeanOfFacility.COMMUNITY_CENTER:
                facility_dict[f'{MeanOfFacility.TOWNHALL - MeanOfFacility.COMMUNITY_CENTER}'] = facility_dict[f'{MeanOfFacility.TOWNHALL - MeanOfFacility.COMMUNITY_CENTER}'] + 1
            if place['tags']['amenity'] in means_of_facility:
                facility_dict[place['tags']['amenity']
                            ] = facility_dict[place['tags']['amenity']] + 1

        except:
            pass

    return facility_dict


async def get_num_facilities_based_location_list_util(locationListConfig: LocationListConfig):

    lat_list, lon_list, distance = astuple(locationListConfig)

    try:
        n = len(lat_list)
        values = await asyncio.gather(*[count_facilities(lat_list[i], lon_list[i], distance, None) for i in range(n)])
        return values
    except Exception as e:
        print("Error in function namely get_num_facilities_based_location_list_util")
        print(e)
        return [{} for _ in range(n)]


async def wrap_facility_info(detailed_location_config: DetailedLocationConfig, facility_count_list):
    means_of_facility_obj = IOReader('json', FilePath.MEAN_OF_FACILITY_DESC).read()
    means_of_facility_list = means_of_facility_obj["means_of_facility_list"]

    lat, lon, district, administrative_genre = astuple(detailed_location_config)

    detailed_location_columns = IOReader('json', FilePath.DETAILED_LOCATION).read()['cols']
    columns = detailed_location_columns + means_of_facility_list

    facility_df = pd.DataFrame(columns=columns)

    lat_list = [lat]
    lon_list = [lon]
    facility_df['lat'] = lat_list
    facility_df['lon'] = lon_list

    facility_df['district'] = [district]
    facility_df['administrative_genre'] = [administrative_genre]

    if len(facility_count_list) > 0:
        values = facility_count_list
    else:
        values = await get_num_facilities_based_location_list_util(LocationListConfig(
            lat_list = lat_list,
            lon_list = lon_list,
            distance = 1000
        ))
    for i, value in enumerate(values):
        for col in means_of_facility_list:
            try:
                facility_df.at[i, col] = value[col]
            except:
                facility_df.at[i, col] = 0

    return facility_df

def cal_distance_to_type_of_place(location_df:pd.DataFrame, place_information_config: PlaceInformationConfig):

    park_df, road_df, commercial_df = astuple(place_information_config)

    park_lat_list = park_df.lat.tolist()
    park_lon_list = park_df.lon.tolist()
    park_cols = [f'park_{i}' for i in range(len(park_df))]
    for i, col in enumerate(park_cols):
        location_df[col] = location_df.apply(lambda x: distance_func(
            x['lat'], x['lon'], park_lat_list[i], park_lon_list[i]), axis=1)

    road_lat_list = road_df.lat.tolist()
    road_lon_list = road_df.lon.tolist()
    road_cols = [f'road_{i}' for i in range(len(road_df))]
    for i, col in enumerate(road_cols):
        location_df[col] = location_df.apply(lambda x: distance_func(
            x['lat'], x['lon'], road_lat_list[i], road_lon_list[i]), axis=1)

    commercial_lat_list = commercial_df.lat.tolist()
    commercial_lon_list = commercial_df.lon.tolist()
    commercial_cols = [f'commercial_{i}' for i in range(len(commercial_df))]

    for col, commercial_lat, commercial_lon, in zip(commercial_cols, commercial_lat_list, commercial_lon_list):
        location_df[col] = location_df.apply(lambda x: distance_func(
            x['lat'], x['lon'], commercial_lat, commercial_lon), axis=1)

    return location_df
