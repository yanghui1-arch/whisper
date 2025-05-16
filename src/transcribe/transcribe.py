
from concurrent.futures import ProcessPoolExecutor

from src.conf import ModelConfig
from src.transcribe import worker
   

class RealtimeTranscribeManager:
    def __init__(self, 
                 config:ModelConfig,
                 max_workers:int=2):
        self.config = config
        self.max_workers = max_workers
        
        self.model_path = self.config.model_path

        self.executor = ProcessPoolExecutor(max_workers=max_workers, initializer=worker._load_model, initargs=(self.model_path,))

    def _transcribe(self, audios:list):
        futures = []
        for task_id, audio in zip(range(len(audios)), audios):
            futures.append(self.executor.submit(worker.transcribe, audio))
        
        for future in futures:
            print("Transcription Result:", future.result())

    def shutdown(self):
        self.executor.shutdown()

tasks = [
    "src/transcribe/test1.mp3",
    "src/transcribe/test.wav"
]

if __name__ == "__main__":
    from src.utils import toml
    conf = toml.transfer_config_toml_to_model_config()
    manager = RealtimeTranscribeManager(config=conf)
    import os
    print(f"Available cpu counts: {os.cpu_count()}")
    manager._transcribe(tasks)