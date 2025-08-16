from pathlib import Path
import threading

from video_tools.model import load_model
from video_tools.ui import make_control_ui
from video_tools.video import run_video_loop


def main():
    project_root = Path(__file__).parent
    # model file lives next to this script or inside the packaged folder
    # prefer the packaged location if present
    packaged = project_root / 'video_tools' / 'yolov8n.pt'
    if packaged.exists():
        model_path = packaged
    else:
        model_path = project_root / 'yolov8n.pt'

    # Events used for cross-thread signaling from the simple Tk UI
    capture_event = threading.Event()
    quit_event = threading.Event()

    # Load model
    model = load_model(model_path)

    # Start UI thread
    start_ui = make_control_ui(capture_event, quit_event)
    ui_thread = threading.Thread(target=start_ui, daemon=True)
    ui_thread.start()

    # Run video loop (blocks until quit)
    run_video_loop(model, capture_event, quit_event)


if __name__ == '__main__':
    main()
