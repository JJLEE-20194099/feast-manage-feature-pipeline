from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FeatureView, FileSource, ValueType

realestate = Entity(
    name="realestate_id",
    value_type=ValueType.INT64,
    description="The ID of the realestate")