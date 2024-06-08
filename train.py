from feast import FeatureStore
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from joblib import dump

store = FeatureStore(repo_path="feature_repo/")

training_df = store.get_saved_dataset(name="realestate_dataset_1").to_df()

labels = training_df['target']
features = training_df.drop(
    labels=['target', 'event_timestamp', "realestate_id"],
    axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, labels)

reg = LinearRegression()
reg.fit(X=X_train[sorted(X_train)], y=y_train)

dump(value=reg, filename="model.joblib")