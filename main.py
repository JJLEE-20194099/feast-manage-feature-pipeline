from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from git import Repo
import pandas as pd
import os

from models.entity import FeatureRepoInfo, FeatureViewInfo


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

    return {
        "entity_names": entity_names,
        "entity_descriptions": entity_descriptions
        }