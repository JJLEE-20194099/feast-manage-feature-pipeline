import pandas as pd
from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
import json

from feature_repo.src.feature_engineering.helper.fv_schema import get_feast_featureset

store = FeatureStore(repo_path="feature_repo/")

HCM_CONFIG = json.load(open('feature_repo/src/config/featureset/full_version.json'))
feature_dict = json.load(open(HCM_CONFIG['featureset_path'], 'r'))
features = feature_dict['cat_cols'] + feature_dict['num_cols']

entity_df = pd.read_parquet(path=HCM_CONFIG['featureset_target_path'])

training_data = store.get_historical_features(
    entity_df=entity_df,
    features=get_feast_featureset(fv_name=HCM_CONFIG['df_feature_view_name'], features = features)
)

dataset = store.create_saved_dataset(
    from_=training_data,
    name=HCM_CONFIG["feast_dataset_name"],
    storage=SavedDatasetFileStorage(HCM_CONFIG["feast_dataset_path"])
)