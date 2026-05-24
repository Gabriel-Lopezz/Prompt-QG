from pathlib import Path
from typing import Literal
import yaml
import datasets
from pydantic import BaseModel, ValidationError

DEFAULT_DATASETS_PATH = Path("./datasets_default.yaml")

class DatasetItem(BaseModel):
    name: str
    rigor: Literal["basic", "standard", "high"]
    topic: str
    source: Literal["hugging_face"] # Only hf support for now
    base_uri: str


class Serializer:
    def __init__(self, add_data_paths: list[str] = []):
        self.dataset_paths = [DEFAULT_DATASETS_PATH]

        user_ds_paths = [Path(filepath) for filepath in add_data_paths]

        for path in user_ds_paths:
            assert path.exists(), f"Given path \"{path}\" cannot be found."
            assert len(path.name) >= 5 and path.name[-5:] == ".yaml", f"File \"{path}\" does not point to a .yaml file."
        
            self.dataset_paths.append(path)
        
        self.datasets = []
        
        for path in self.dataset_paths:
            self.datasets.extend(self.yaml_as_dataset_list(path))
    
    def yaml_as_dataset_list(self, dataset_path: Path):

        with open(dataset_path) as dataset_file:
            # Load datasets; DatasetItem class enforces attributes
            file_datasets = yaml.safe_load(dataset_file)
        
        dataset_items = [DatasetItem(**ds) for ds in file_datasets]
        return dataset_items        

class hugging_face_handler:
    
    def __init__(self, items: list[DatasetItem]):
        pass

### Tests
if __name__ == "__main__":
    s = Serializer()
    print(s.datasets)

