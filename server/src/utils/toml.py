import os
import tomllib
from pathlib import Path
from dataclasses import fields

from src.conf import ModelConfig

CURRENT_FILE_PATH: Path = Path(__file__).resolve()
config_path:Path = CURRENT_FILE_PATH.parent.parent.parent / "config.toml"

def transfer_config_toml_to_model_config():
    print("Config file is at {}".format(config_path))
    with open(config_path, "rb") as f:
        _config = tomllib.load(f)
        config_fields = {f.name for f in fields(ModelConfig)}
        config = {k: v for k, v in _config['model'].items() if k in config_fields}
    return ModelConfig(**config)