from datetime import timedelta
from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType

from src.constants.file_path import DATA_FEATURE_SET1, DATA_FEATURE_SET2, DATA_FEATURE_SET3, DATA_FEATURE_SET4, DATA_TARGET

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.STRING,
    description="The ID of the realestate")

f_source1 = FileSource(
    path=DATA_FEATURE_SET1,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df1_fv = FeatureView(
    name="df1_feature_view",
    ttl=timedelta(days=3),
    entities=[realestate],
    schema=[
        Field(name="num_of_bathroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="district", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32])
        ],
    source=f_source1
)

f_source2 = FileSource(
    path=DATA_FEATURE_SET2,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df2_fv = FeatureView(
    name="df2_feature_view",
    ttl=timedelta(days=3),
    entities=[realestate],
    schema=[
        Field(name="num_of_bathroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="district", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32])
        ],
    source=f_source2
)


f_source3 = FileSource(
    path=DATA_FEATURE_SET3,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df3_fv = FeatureView(
    name="df3_feature_view",
    ttl=timedelta(days=3),
    entities=[realestate],
    schema=[
        Field(name="num_of_bathroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="district", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="num_of_bedroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        ],
    source=f_source3
)

f_source4 = FileSource(
    path=DATA_FEATURE_SET4,
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

df4_fv = FeatureView(
    name="df4_feature_view",
    ttl=timedelta(days=3),
    entities=[realestate],
    schema=[
        Field(name="num_of_bathroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="district", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="num_of_bedroom", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        Field(name="used_area", dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32]),
        ],
    source=f_source4
)

target_source = FileSource(
    path=DATA_TARGET,
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
    source=target_source
)