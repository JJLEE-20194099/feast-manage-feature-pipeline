# import pandas as pd
# import json
# from tqdm import tqdm

# from src.feature_engineering.facility.constant import FilePath
# from src.feature_engineering.facility.service import count_facilities

# means_of_facility_obj = json.load(open(FilePath.MEAN_OF_FACILITY_DESC, encoding='utf-8'))
# means_of_facility = means_of_facility_obj["means_of_facility_list"]

# num_of_facility_dict = {}
# for facility in means_of_facility:
#     num_of_facility_dict[facility] = []

# latlon_df = pd.read_csv('src/feature_engineering/facility/data/table/hcm_hn_latlon.csv')

# distance = 1000

# lat_list = latlon_df['lat'].tolist()
# lon_list = latlon_df['lon'].tolist()

# for (lat, lon) in tqdm(zip(lat_list, lon_list)):
#     num_of_facility = count_facilities(lat, lon, distance=distance)

#     for facility in means_of_facility:
#         num_of_facility_dict[facility].append(num_of_facility[facility])
# df= pd.DataFrame(columns = ['lat', 'lon'] + means_of_facility)
# df['lat'] = lat_list
# df['lon'] = lon_list
# for facility in means_of_facility:
#     df[facility] = num_of_facility_dict[facility]

# df.to_csv(f'./data/table/hcm_hn_distance_{distance}_facility_count.csv', index=False)