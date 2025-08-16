import cv2
import time
from pathlib import Path
from datetime import datetime


def run_video_loop(model, capture_event, quit_event, window_name='Object detection'):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    print('Starting video capture. Press q to quit.')

    frame_count = 0
    acc_infer = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            t0 = time.perf_counter()
            results = model(frame)
            infer_time = time.perf_counter() - t0
            frame_count += 1
            acc_infer += infer_time

            res = results[0] if isinstance(results, (list, tuple)) else results
            if hasattr(res, 'plot'):
                annotated_frame = res.plot()
            else:
                annotated_frame = frame

            # If annotated_frame is a PIL Image, convert to BGR numpy array
            try:
                from PIL import Image
                import numpy as np
                if isinstance(annotated_frame, Image.Image):
                    annotated_frame = cv2.cvtColor(np.array(annotated_frame), cv2.COLOR_RGB2BGR)
            except Exception:
                pass

            # If the UI requested a capture, save the current annotated frame
            if capture_event.is_set():
                try:
                    caps_dir = Path('captures')
                    caps_dir.mkdir(exist_ok=True)
                    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                    out_name = caps_dir / f'capture_{ts}.jpg'
                    cv2.imwrite(str(out_name), annotated_frame)
                    print(f"Captured frame saved to {out_name}")
                except Exception as cap_err:
                    print(f"Failed to save captured frame: {cap_err}")
                finally:
                    capture_event.clear()

            # If the UI requested quit, break the loop cleanly
            if quit_event.is_set():
                print('Quit requested from control UI')
                break

            try:
                cv2.imshow(window_name, annotated_frame)
            except Exception as imshow_err:
                out_path = Path('frame_last.jpg')
                try:
                    cv2.imwrite(str(out_path), annotated_frame)
                    print(f"Could not open window (headless?). Saved last frame to {out_path}")
                except Exception as save_err:
                    print(f"Failed to write fallback frame: {save_err}")
                break

            if frame_count % 30 == 0:
                avg = acc_infer / frame_count if frame_count else 0
                print(f"Frames: {frame_count}, last_infer={infer_time:.3f}s, avg_infer={avg:.3f}s")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
