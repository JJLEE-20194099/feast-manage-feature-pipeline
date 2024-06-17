from datetime import timedelta
from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType

from src.constants.file_path import DATA_FEATURE_SET_HCM, DATA_TARGET_HCM

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.STRING,
    description="The ID of the realestate")

df_source_hcm = FileSource(
    path=DATA_FEATURE_SET_HCM,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df_hcm_fv = FeatureView(
    name="df_hcm_feature_view",
    ttl=timedelta(days=3),
    entities=[realestate],
    schema=[
        Field(name="num_of_bathroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="district", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="num_of_bedroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="used_area", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        ],
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