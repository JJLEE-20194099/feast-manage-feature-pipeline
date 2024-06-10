from typing import Union, List
from dataclasses import dataclass
import pandas as pd

Num = Union[int, float]

@dataclass
class LocationConfig:
    lat: float
    lon: float
    distance: int

@dataclass
class DetailedLocationConfig:
    lat: float
    lon: float
    district: str
    administrative_genre: str

@dataclass
class PlaceInformationConfig:
    park_df: pd.DataFrame
    road_df: pd.DataFrame
    commercial_df: pd.DataFrame

@dataclass
class LocationListConfig:
    lat_list: List[Num]
    lon_list: List[Num]
    distance: int
