from pathlib import Path
import time
from ultralytics import YOLO


def load_model(model_path: str | Path = 'yolov8n.pt'):
    """Load a YOLO model from disk or download it if missing.

    Returns the instantiated model object.
    """
    model_path = Path(model_path)
    if not model_path.exists():
        print(f"{model_path} not found locally — ultralytics will attempt to download the weights if internet is available.")
    print(f"Loading YOLO model from '{model_path}' (this may download weights).")
    load_start = time.perf_counter()
    model = YOLO(str(model_path))
    load_elapsed = time.perf_counter() - load_start
    print(f"Model loaded successfully in {load_elapsed:.1f}s")
    return model
