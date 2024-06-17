from datetime import timedelta
from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType
import json

from src.feature_engineering.helper.fv_schema import get_fv_schema_by_path

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.STRING,
    description="The ID of the realestate")


HCM_CONFIG = json.load(open('src/config/featureset/full_version.json'))
hcm_featureset_path = HCM_CONFIG['featureset_path']

df_source_hcm = FileSource(
    path=HCM_CONFIG['featureset_df_path'],
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df_hcm_fv = FeatureView(
    name=HCM_CONFIG['df_feature_view_name'],
    ttl=timedelta(days=3),
    entities=[realestate],
    schema= get_fv_schema_by_path(path = hcm_featureset_path),
    source=df_source_hcm
)

target_source_hcm = FileSource(
    path=HCM_CONFIG['featureset_target_path'],
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

target_fv = FeatureView(
    name=HCM_CONFIG['target_feature_view_name'],
    entities=[realestate],
    ttl=timedelta(days=100),
    schema=[
        Field(name="target", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.FLOAT])
        ],
    source=target_source_hcm
)