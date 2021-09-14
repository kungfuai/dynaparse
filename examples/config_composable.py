from pydantic import BaseModel

from typing import List


class ModelConfig(BaseModel):
    model_type: str = "boosted_tree"


class DataConfig(BaseModel):
    paths: List[str] = ["path1"]
    augmentation: bool = False


class TrainingConfig(BaseModel):
    data = DataConfig(paths=["train/data1", "train/data2"], augmentation=True)
    epochs: int = 100
    learning_rate: float = 1e-4


class EvaluationConfig(BaseModel):
    data = DataConfig(paths=["val/data1"], augmentation=False)


class ExperimentConfig(BaseModel):
    model = ModelConfig()
    training = TrainingConfig()
    evaluation = EvaluationConfig()
