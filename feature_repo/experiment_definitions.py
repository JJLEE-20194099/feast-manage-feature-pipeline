from datetime import timedelta
from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType
import json
from tqdm import tqdm

from src.feature_engineering.helper.fv_schema import get_fv_schema_by_path

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.STRING,
    description="The ID of the realestate")

fv_list = []


for city in ['hn', 'hcm']:
    for version in tqdm(range(6)):
        path = f"./src/config/featureset/update_data/mlops_exp1/{city}_v{version}.json"

        CONFIG = json.load(open(path, encoding='utf-8'))
        featureset_path = CONFIG['featureset_path']


        fv_list.append(FeatureView(
            name=CONFIG['df_feature_view_name'],
            ttl=timedelta(days=3),
            entities=[realestate],
            schema= get_fv_schema_by_path(path = featureset_path),
            source=FileSource(
            path=CONFIG['featureset_df_path'],
            timestamp_field="event_timestamp",
        )
        ))


        fv_list.append(FeatureView(
            name=CONFIG['target_feature_view_name'],
            entities=[realestate],
            ttl=timedelta(days=100),
            schema=[
                Field(name="target", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.FLOAT])
                ],
            source=FileSource(
            path=CONFIG['featureset_target_path'],
            timestamp_field="event_timestamp",
        )
        ))

fv0 = fv_list[0]
fv1 = fv_list[1]
fv2 = fv_list[2]
fv3 = fv_list[3]
fv4 = fv_list[4]
fv5 = fv_list[5]
fv6 = fv_list[6]
fv7 = fv_list[7]
fv8 = fv_list[8]
fv9 = fv_list[9]
fv10 = fv_list[10]
fv11 = fv_list[11]
fv12 = fv_list[12]
fv13 = fv_list[13]
fv14 = fv_list[14]
fv15 = fv_list[15]
fv16 = fv_list[16]
fv17 = fv_list[17]
fv18 = fv_list[18]
fv19 = fv_list[19]
fv20 = fv_list[20]
fv21 = fv_list[21]
fv22 = fv_list[22]
fv23 = fv_list[23]
