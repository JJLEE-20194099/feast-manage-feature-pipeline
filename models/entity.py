from pydantic import BaseModel
class EntityDF(BaseModel):
    entity_keys: list[int]
    entity_name: str
    timestamps: list[str]
    frequency: str

class SaveDatasetInfo(BaseModel):
    dataset_name: str
    feature_view_names: list[str]
    dest_folder_path: str

class FeatureRepoInfo(BaseModel):
    path: str

class FeatureViewInfo(BaseModel):
    name: str

class MLOpsExpData(BaseModel):
    version_tag:str