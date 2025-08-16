import threading
from datetime import datetime
try:
    import tkinter as tk
    from tkinter import ttk
except Exception:
    tk = None


def make_control_ui(capture_event, quit_event):
    """Return a function that starts the Tk control window when called.

    Designed to be run on a background thread.
    """

    def start_control_window():
        if tk is None:
            print("Tkinter not available: GUI capture button won't be shown.")
            return

        root = tk.Tk()
        root.title('Controls')
        root.geometry('220x80')

        def on_capture():
            capture_event.set()

        def on_quit():
            quit_event.set()
            root.destroy()

        frm = ttk.Frame(root, padding=10)
        frm.pack(fill='both', expand=True)
        btn_capture = ttk.Button(frm, text='Capture Frame', command=on_capture)
        btn_capture.pack(fill='x', pady=(0, 6))
        btn_quit = ttk.Button(frm, text='Quit', command=on_quit)
        btn_quit.pack(fill='x')

        try:
            root.mainloop()
        except Exception:
            return

    return start_control_window
