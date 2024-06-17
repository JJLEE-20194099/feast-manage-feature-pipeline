from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float32, Float64, Int64, String, Int32, VALUE_TYPES_TO_FEAST_TYPES
from feast.value_type import ValueType
import json

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

def get_fv_schema_by_path(path = '/home/long/long/datn-feast/data/featureset/full_version.json'):
    feature_set = json.load(open(path, 'r'))
    cat_cols = feature_set['cat_cols']
    num_cols = feature_set['num_cols']

    cat_fv_schema = create_fv_schema(cat_cols, feature_type='cat')
    num_fv_schema = create_fv_schema(num_cols, feature_type='num')


    return cat_fv_schema + num_fv_schema

def get_feast_featureset(fv_name, features):
    return [f'{fv_name}:{feature}' for feature in features]