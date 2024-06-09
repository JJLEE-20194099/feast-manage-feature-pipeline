from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from git import Repo
import pandas as pd
import os

from models.entity import EntityDF, FeatureRepoInfo, FeatureViewInfo, SaveDatasetInfo


app = FastAPI(
    title='ĐATN - Feast - API Documentation', docs_url='/docs',
    dependencies=[
        # Depends(get_query_token),
        # Depends(reusable_oauth2)
    ]
)
# Allow all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_store")
def get_store(body: FeatureRepoInfo):
    body = dict(body)
    app.store = FeatureStore(
        repo_path=body['path']
    )

    app.repo_path = body['path']

    os.chdir(app.repo_path)

    os.system("feast teardown")
    os.system("feast apply")

    os.chdir("../")

    return "Feast teardown & feast apply to register feature done"

@app.get("/get_feature_views")
def get_feature_views():
    feature_views = app.store.list_feature_views()
    feature_view_names = []

    for feature_view in feature_views:
        feature_view_names.append(feature_view.name)

    return {"feature_view_names": feature_view_names}

@app.post("/get_feature_names")
def get_feature_names(body: FeatureViewInfo):

    feature_view_name = dict(body)['name']
    feature_names = []


    for feature in app.store.get_feature_view(name=feature_view_name).features:
        feature_names.append(feature.name)

    return {"feature_names": feature_names}

@app.get("/get_entities")
def get_entities():
    entities = app.store.list_entities()

    entity_names = []
    entity_descriptions = []

    for entity in entities:
        entity_names.append(entity.name)
        entity_descriptions.append(entity.description)
        print(entity)

    return {
        "entity_names": entity_names,
        "entity_descriptions": entity_descriptions
        }


from datetime import datetime, timedelta

end_date=pd.Timestamp.now()
start_date=pd.Timestamp.now() - pd.Timedelta(3, 'day')

@app.post("/register_entity_df")
def register_entity_df(entity_df_params: EntityDF):
    timestamps = pd.date_range(
        end=end_date,
        start=start_date,
        freq=entity_df_params.frequency
    ).to_frame(
        index=False,
        name="event_timestamp"
        )

    entity_ids = pd.DataFrame(
        data=entity_df_params.entity_keys,
        columns=[entity_df_params.entity_name]
        )
    entity_df = timestamps.merge(
        right=entity_ids,
        how="cross"
        )
    app.entity_df = entity_df

@app.post("/save_dataset")
def save_dataset(dataset_info: SaveDatasetInfo):

    dataset_info = dict(dataset_info)
    features_to_get = []

    for feature_view in dataset_info['feature_view_names']:
        for feature in app.store.get_feature_view(name=feature_view).features:
            features_to_get.append(feature_view + ":" + feature.name)

    job = app.store.get_historical_features(
        entity_df=app.entity_df, features=features_to_get
    )

    storage_path = os.path.join(
        dataset_info["dest_folder_path"],
        f"{dataset_info['dataset_name']}.parquet",
    )

    app.store.create_saved_dataset(
        from_=job,
        name=dataset_info['dataset_name'],
        storage=SavedDatasetFileStorage(storage_path),
    )
