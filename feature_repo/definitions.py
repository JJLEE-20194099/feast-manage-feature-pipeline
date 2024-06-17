from datetime import timedelta
from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType

from src.feature_engineering.helper.fv_schema import get_fv_schema_by_path
from src.constants.file_path import DATA_FEATURE_SET_HCM, DATA_TARGET_HCM

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.STRING,
    description="The ID of the realestate")

hcm_featureset_path = '/home/long/long/datn-feast/data/featureset/full_version.json'

df_source_hcm = FileSource(
    path=DATA_FEATURE_SET_HCM,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df_hcm_fv = FeatureView(
    name="df_hcm_feature_view",
    ttl=timedelta(days=3),
    entities=[realestate],
    schema= get_fv_schema_by_path(path = hcm_featureset_path),
    source=df_source_hcm
)

target_source_hcm = FileSource(
    path=DATA_TARGET_HCM,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

target_fv = FeatureView(
    name="target_feature_view",
    entities=[realestate],
    ttl=timedelta(days=3),
    schema=[
        Field(name="target", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.FLOAT])
        ],
    source=target_source_hcm
)