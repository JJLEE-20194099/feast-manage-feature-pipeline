from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType

def create_fv_schema(features, feature_type = 'cat'):
    if feature_type == 'num':
        return [
                Field(name=feature, dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.FLOAT])
                for feature in features
            ]
    return [
                Field(name=feature, dtype=VALUE_TYPES_TO_FEAST_TYPES[ValueType.INT32])
                for feature in features
            ]
