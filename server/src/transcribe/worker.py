import os

from transformers.pipelines.base import Pipeline
from transformers import PreTrainedModel

model:PreTrainedModel = None
processor = None
pipe:Pipeline = None

def _load_model(model_path):
    global model, processor, pipe
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

    pid = os.getpid()
    print(f"PID: {pid} ----------> loading model...")

    model_path = "openai/whisper-large-v3"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path, torch_dtype=torch.float16, low_cpu_mem_usage=True).to("cpu")
    processor = AutoProcessor.from_pretrained(model_path)
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch.float16,
        device="cpu",
    )

def transcribe(audio:str, **kwargs):
    global pipe
    result = pipe(audio)
    print(result['text'])
    return result['text']