import pandas as pd
from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
import json
import os
from feature_repo.src.feature_engineering.helper.fv_schema import get_feast_featureset
from tqdm import tqdm

store = FeatureStore(repo_path="feature_repo/")

for city in ['hn', 'hcm']:
    for version in tqdm(range(5)):
        path = f"feature_repo/src/config/featureset/{city}_v{version}.json"

        CONFIG = json.load(open(path, encoding='utf-8'))

        feature_dict = json.load(open(CONFIG['featureset_path'], 'r', encoding='utf-8'))
        features = feature_dict['cat_cols'] + feature_dict['num_cols']

        entity_df = pd.read_parquet(path=CONFIG['featureset_target_path'])

        try:
            os.remove(CONFIG["feast_dataset_path"])
        except:pass

        training_data = store.get_historical_features(
            entity_df=entity_df,
            features=get_feast_featureset(fv_name=CONFIG['df_feature_view_name'], features = features)
        )

        try:
            dataset = store.create_saved_dataset(
                from_=training_data,
                name=CONFIG["feast_dataset_name"],
                storage=SavedDatasetFileStorage(CONFIG["feast_dataset_path"])
            )
        except:
            print(f"Existed Dataset - {CONFIG['feast_dataset_name']}")