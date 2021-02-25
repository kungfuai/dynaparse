from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json
from dataclasses_jsonschema import JsonSchemaMixin


@dataclass_json
@dataclass
class Config(JsonSchemaMixin):
    """testing"""

    train_split_proportion: float
    conv_activation: str
    conv_padding: str
    dense_inter_size: int
    max_pool_filter_size: int
    in_shape: List[int]
    max_num_signatures_per_grab: int
    grab_label_file: str
    length: int
    signal_prop: float
    signal_nonconflation_prop: float
    val_signal_nonconflation_prop: float
    kernel_sizes: List[int]
    filter_sizes: List[int]
    network: str = "test"


if __name__ == "__main__":
    from jsonargparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_class_arguments(Config)
    args = parser.parse_args()