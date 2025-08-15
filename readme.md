# video-tools

Lightweight utilities for running YOLOv8 object detection on webcam or video, capturing annotated frames, and a small Tk UI for user-controlled captures.

This repo contains a simple demo that uses Ultralytics YOLO, OpenCV, and a tiny Tkinter control window.

Features
- Load YOLOv8 weights (will be downloaded automatically when missing)
- Real-time webcam inference and annotated display
- Clickable "Capture Frame" button to save annotated frames to the `captures/` folder
- Graceful shutdown via the UI or pressing `q`

Structure
- `load-model.py` — top-level script that orchestrates the app
- `video_tools/` — small package with the main components:
	- `video_tools/model.py` — model loading helper
	- `video_tools/video.py` — video capture + inference loop
	- `video_tools/ui.py` — small Tk UI (Capture / Quit)
- `captures/` — saved annotated frames
- `yolov8n.pt` — model weights (optional; will be downloaded automatically)

Quick start (Windows PowerShell)

1. Install dependencies and create the virtual environment using Poetry (if not already):

```powershell
# run from the nested project folder where pyproject.toml is located
Set-Location 'C:\Users\xxxx\python\video-tools\video-tools'
poetry install
```

2. Run the app:

```powershell
poetry run python ..\load-model.py
```

3. Use the Control window:
- Click "Capture Frame" to save the currently displayed annotated frame to `captures/`.
- Click "Quit" (or press `q` in the OpenCV window) to exit.

Notes & Troubleshooting
- If the script cannot find `yolov8n.pt`, Ultralytics will attempt to download it. Ensure you have internet access for the first run.
- On headless systems (no GUI), the script will save the last frame to `frame_last.jpg` if it cannot open an OpenCV window.
- If you don't have Tkinter available, the capture UI will not be shown — the script will still run and you can capture frames by programmatic triggers.

Suggested next steps
- Add a small CLI or config file to choose between camera devices or a video file input.
- Save detection metadata (bounding boxes, class ids, scores) alongside images as JSON.
- Add tests around model loading and the capture functionality.

License
- MIT

