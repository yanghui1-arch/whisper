from enum import Enum
from dataclasses import dataclass

@dataclass
class ModelConfig:
    model_path:str
    sample_rate:int
    gpu_use:bool

class ClientConfig:
    inactivity_threshold:float=1
    min_audio_seconds:float=0.5
