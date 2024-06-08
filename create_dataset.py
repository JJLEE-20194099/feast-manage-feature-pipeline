import pandas as pd
from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage

store = FeatureStore(repo_path="feature_repo/")

entity_df = pd.read_parquet(path="data/target_df.parquet")

training_data = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "df4_feature_view:num_of_bathroom",
        "df4_feature_view:district",
        "df4_feature_view:num_of_bedroom",
        "df4_feature_view:used_area"
    ]
)

dataset = store.create_saved_dataset(
    from_=training_data,
    name="realestate_dataset_1",
    storage=SavedDatasetFileStorage("data/realestate_dataset_1.parquet")
)