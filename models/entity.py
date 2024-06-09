from pydantic import BaseModel
class EntityDF(BaseModel):
    entity_keys: list[int]
    entity_name: str
    timestamps: list[str]
    frequency: str

class SaveDatasetInfo(BaseModel):
    dataset_name: str
    feature_view_names: list[str]

class FeatureRepoInfo(BaseModel):
    path: str

class FeatureViewInfo(BaseModel):
    name: str