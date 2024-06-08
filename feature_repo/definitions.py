from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FeatureView, FileSource, ValueType

from src.constants.file_path import DATASET_PATH

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.INT64,
    description="The ID of the realestate")

f_source1 = FileSource(
    path=DATASET_PATH,
    event_timestamp_column="event_timestamp"
)