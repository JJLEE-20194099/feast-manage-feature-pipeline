from feast import FeatureStore
import pandas as pd
from joblib import load

store = FeatureStore(repo_path="feature_repo/")

feast_features = [
        "df4_feature_view:num_of_bathroom",
        "df4_feature_view:district",
        "df4_feature_view:num_of_bedroom",
        "df4_feature_view:used_area"
    ]


features = store.get_online_features(
    features=feast_features,
    entity_rows=[{"realestate_id": 42774}, {"realestate_id": 42773}]
).to_dict()

features_df = pd.DataFrame.from_dict(data=features)
print(features_df)

reg = load("model.joblib")
predictions = reg.predict(
    features_df[sorted(features_df.drop("realestate_id", axis=1))])

print(predictions)