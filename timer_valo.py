import tkinter as tk
from tkinter import messagebox
import threading
import time
import cv2
import numpy as np
import mss
import base64
import ctypes
import pystray
from PIL import Image, ImageDraw
import sys

# --- Core Parameters ---
CANNY_THRESHOLDS = (100, 200)   # Edge detection thresholds
DETECTION_THRESHOLD = 0.15      # Match score must be higher than this to trigger
SCAN_INTERVAL_S = 0.05          # Screen scan interval when searching for Spike (seconds)
SCAN_INTERVAL_COUNTDOWN_S = 0.2 # Slower scan when countdown active (saves CPU)
COUNTDOWN_SECONDS = 45          # Total countdown duration for the Spike
COOLDOWN_PERIOD_S = 50          # Cooldown after a detection to prevent re-triggering

# --- Image Data (Base64) ---
IMAGE_DATA = {
    '1k': '''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''',
    '2k': '''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''',
}

# --- Resolution Configurations ---
RESOLUTION_SETTINGS = {
    '1k': {
        'description': '1K (1920x1080)',
        'roi': {'left': 918,  'top': 15, 'width': 84,  'height': 75},
        'b64_data': IMAGE_DATA['1k']
    },
    '2k': {
        'description': '2K (2560x1440)',
        'roi': {'left': 1225, 'top': 20, 'width': 110, 'height': 100},
        'b64_data': IMAGE_DATA['2k']
    },
    '4:3': {
        'description': '4:3 (1440x1080)',
        'roi': {'left': 658, 'top': 0, 'width': 106, 'height': 94},
        'b64_data': IMAGE_DATA['1k']  # Sử dụng cùng template với 1k
    }
}

# Global state variables
stop_event = threading.Event()
last_detection_time = 0
countdown_active = False  # Track if countdown is currently running

class OverlayWindow(tk.Toplevel):
    """Base class for all overlay windows, encapsulating common settings."""
    def __init__(self, master, geometry_str):
        super().__init__(master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "black")
        self.geometry(geometry_str)

class ScoreDisplay(OverlayWindow):
    """A window to display the match score for debugging."""
    def __init__(self, master):
        # Adjust position dynamically based on screen width
        screen_width = master.winfo_screenwidth()
        x_pos = screen_width - 250 if screen_width < 1920 else 1600
        super().__init__(master, f"+{x_pos}+50")
        self.label = tk.Label(self, text="...", font=("Helvetica", 16), fg="white", bg="black")
        self.label.pack(pady=10, padx=10)
        self.last_high_score_time = 0

    def update_score(self, score):
        # To make it easier to observe, "freeze" the high score on screen for 3 seconds
        if score >= DETECTION_THRESHOLD:
            self.label.config(text=f"Match: {score:.3f}", fg="lime")
            self.last_high_score_time = time.time()
        elif time.time() - self.last_high_score_time > 3:
            self.label.config(text=f"Match: {score:.3f}", fg="white")

class CountdownTimer(OverlayWindow):
    """Displays a large countdown timer on the screen."""
    def __init__(self, master):
        super().__init__(master, "+20+20") # Default to top-left corner
        self.label = tk.Label(self, text="", font=("Helvetica", 32, "bold"), fg="white", bg="black")
        self.label.pack(pady=15, padx=15)
        self.job_id = None
        self.withdraw() # Hidden by default

    def start(self, score):
        global last_detection_time, countdown_active
        if time.time() - last_detection_time < COOLDOWN_PERIOD_S:
            return

        last_detection_time = time.time()
        countdown_active = True
        print(f"Detection successful (Match: {score:.3f}), starting countdown window.")

        end_time = time.time() + COUNTDOWN_SECONDS
        if self.job_id: self.after_cancel(self.job_id) # Cancel previous countdown
        self.deiconify() # Show window
        self.tick(end_time)

    def stop(self):
        """Stop countdown immediately (called when round ends)"""
        global countdown_active
        countdown_active = False
        if self.job_id:
            self.after_cancel(self.job_id)
            self.job_id = None
        print("Countdown stopped - Round ended")
        self.withdraw()

    def tick(self, end_time):
        global countdown_active
        remaining = end_time - time.time()
        
        # Stop if countdown was cancelled or time is up
        if not countdown_active or remaining <= 0:
            self._update_display(0 if remaining <= 0 else remaining)
            if remaining <= 0:
                print("Countdown finished.")
            countdown_active = False
            self.withdraw()
        else:
            self._update_display(remaining)
            self.job_id = self.after(50, self.tick, end_time) # Refresh every 50ms

    def _update_display(self, remaining_time):
        if remaining_time <= 7: color = "#ff4757"  # Red
        elif remaining_time <= 14: color = "#ffa502" # Orange
        else: color = "white"
        
        # Show one decimal place in the last 10 seconds for added tension
        text = f"{remaining_time:.1f}" if 0 < remaining_time <= 10 else f"{int(round(remaining_time))}"
        self.label.config(text=text, fg=color)


def prepare_template(b64_string):
    """Decodes from Base64 string and prepares the edge image for matching."""
    try:
        decoded_data = base64.b64decode(b64_string)
        np_array = np.frombuffer(decoded_data, np.uint8)
        template_img = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

        if template_img is None: raise ValueError("Could not decode image from Base64")
        if template_img.shape[2] != 4: raise ValueError("Image must be a PNG with an Alpha channel")

        alpha_mask = template_img[:, :, 3]
        bgr_icon = template_img[:, :, :3]
        # Create a perfect icon without background interference for edge detection
        perfect_icon = cv2.bitwise_and(bgr_icon, bgr_icon, mask=alpha_mask)
        return cv2.Canny(perfect_icon, *CANNY_THRESHOLDS)
    except Exception as e:
        messagebox.showerror("Template Error", f"Error processing built-in image data: {e}")
        return None


def detector_thread_func(root, config, countdown_win, score_win):
    global countdown_active
    template_edges = prepare_template(config['b64_data'])
    if template_edges is None:
        root.after(0, root.destroy) # Close the app if template loading fails
        return

    print(f"Detection started for {config['description']} - ROI: {config['roi']}")
    print(f"Scan rate: {1/SCAN_INTERVAL_S:.1f} FPS (normal), {1/SCAN_INTERVAL_COUNTDOWN_S:.1f} FPS (countdown)")
    if score_win:
        print(f"Debug window position: {score_win.winfo_x()}, {score_win.winfo_y()}")

    # Track consecutive low detections to determine round end
    consecutive_low_detections = 0
    REQUIRED_LOW_DETECTIONS = 10  # Need 10 consecutive low scores (0.5s) to confirm round end
    LOW_DETECTION_THRESHOLD = 0.05  # Much lower than normal threshold
    
    # Performance optimization: reuse numpy arrays
    last_screenshot = None
    frame_skip_counter = 0
    FRAME_SKIP_DURING_COUNTDOWN = 2  # Skip 2 frames when countdown active (further CPU saving)

    with mss.mss() as sct:
        while not stop_event.is_set():
            # Adaptive scan rate: slower when countdown is active to save CPU
            current_interval = SCAN_INTERVAL_COUNTDOWN_S if countdown_active else SCAN_INTERVAL_S
            
            # Frame skipping during countdown for additional CPU saving
            if countdown_active:
                frame_skip_counter += 1
                if frame_skip_counter < FRAME_SKIP_DURING_COUNTDOWN:
                    time.sleep(current_interval)
                    continue
                frame_skip_counter = 0
            
            screenshot = np.array(sct.grab(config['roi']))
            screen_edges = cv2.Canny(screenshot, *CANNY_THRESHOLDS)
            
            result = cv2.matchTemplate(screen_edges, template_edges, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            # Update UI
            if score_win and score_win.winfo_exists():
                root.after(0, score_win.update_score, max_val)

            # Check if Spike icon is detected (start countdown)
            if max_val >= DETECTION_THRESHOLD:
                root.after(0, countdown_win.start, max_val)
                consecutive_low_detections = 0  # Reset counter when Spike is detected
            
            # Check if Spike icon disappeared (round ended)
            elif countdown_active:
                if max_val < LOW_DETECTION_THRESHOLD:
                    consecutive_low_detections += 1
                    if consecutive_low_detections >= REQUIRED_LOW_DETECTIONS:
                        # Spike icon has been gone for 0.5s, round likely ended
                        print(f"Spike icon disappeared (score: {max_val:.3f}), stopping countdown")
                        root.after(0, countdown_win.stop)
                        consecutive_low_detections = 0
                else:
                    # Reset if we get a slightly higher score (might be noise)
                    consecutive_low_detections = 0

            time.sleep(current_interval)
    
    print("Background detection thread has stopped.")
    # When the thread ends, destroy the windows it created
    for win in (score_win, countdown_win):
        if win and win.winfo_exists():
            win.destroy()


def main():
    # Force DPI awareness to prevent scaling issues on high-DPI screens
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception as e:
        print(f"Warning: Failed to set DPI awareness, {e}")

    # --- Window Initialization ---
    root = tk.Tk()
    root.title("Valorant Spike Timer")
    root.geometry("600x430")
    root.minsize(600, 430)
    root.resizable(False, False)
    root.configure(bg='#0f1923')
    
    # Set window icon
    try:
        import os
        import sys
        
        # Get the correct path for icon (works for both script and exe)
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            application_path = sys._MEIPASS
        else:
            # Running as script
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(application_path, 'icon_ultra_sharp.ico')
        
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            print(f"Icon file not found at: {icon_path}")
    except Exception as e:
        print(f"Could not set window icon: {e}")

    # colors & simple theme
    style = {
        'bg': '#0f1923',
        'fg': '#ece8e1',
        'accent': '#ff4655',
        'panel': '#151b21',
        'muted': '#8a8a8a',
        'btn': '#1c252e',
        'btn_hover': '#26333b'
    }

    # small helper: tooltip
    class ToolTip(object):
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tip = None
            widget.bind("<Enter>", self.show)
            widget.bind("<Leave>", self.hide)
        def show(self, _e=None):
            if self.tip: return
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            self.tip = tk.Toplevel(self.widget)
            self.tip.wm_overrideredirect(True)
            self.tip.wm_geometry(f"+{x}+{y}")
            lbl = tk.Label(self.tip, text=self.text, bg=style['panel'], fg=style['fg'], font=("Segoe UI", 8), bd=1, relief='solid', padx=6, pady=3)
            lbl.pack()
        def hide(self, _e=None):
            if self.tip:
                self.tip.destroy()
                self.tip = None

    # Header
    header = tk.Frame(root, bg=style['bg'])
    header.grid(row=0, column=0, sticky='ew', pady=(18,8), padx=12)
    root.grid_columnconfigure(0, weight=1)

    # Title with better styling
    title_frame = tk.Frame(header, bg=style['bg'])
    title_frame.pack()
    lbl_title = tk.Label(title_frame, text="VALORANT SPIKE TIMER", font=("Segoe UI", 20, 'bold'), fg=style['accent'], bg=style['bg'], pady=2)
    lbl_title.pack()
    
    # Subtitle with icon
    lbl_sub = tk.Label(header, text="⚡ Auto-detect spike and show a 45s overlay", font=("Segoe UI", 9), fg=style['muted'], bg=style['bg'])
    lbl_sub.pack()

    # main panel with card styling
    panel_wrapper = tk.Frame(root, bg=style['bg'])
    panel_wrapper.grid(row=1, column=0, padx=20, pady=(0,12), sticky='nsew')
    
    panel = tk.Frame(panel_wrapper, bg=style['panel'], bd=0, relief='flat', highlightthickness=1, highlightbackground='#2a3744')
    panel.pack(fill='both', expand=True)

    # Resolution title
    res_title = tk.Label(panel, text="SELECT RESOLUTION", font=("Segoe UI", 9, 'bold'), fg=style['muted'], bg=style['panel'])
    res_title.pack(pady=(15, 8))

    # Resolution buttons with card style
    btn_row = tk.Frame(panel, bg=style['panel'])
    btn_row.pack(padx=15, pady=(0, 12))

    buttons = {}
    res_cfg = [('1k','1920 × 1080','Full HD'), ('2k','2560 × 1440','2K'), ('4:3','1440 × 1080','4:3')]
    for i,(k, label_txt, small) in enumerate(res_cfg):
        container = tk.Frame(btn_row, bg=style['panel'])
        container.grid(row=0, column=i, padx=10)
        
        # Styled button with border
        b = tk.Button(container, text=label_txt, font=("Segoe UI", 11, 'bold'), 
                     bg=style['btn'], fg=style['fg'], 
                     activebackground=style['accent'], activeforeground='white', 
                     width=13, height=2, bd=0, cursor='hand2', relief='flat',
                     highlightthickness=1, highlightbackground='#2a3744')
        b.pack(pady=3)
        
        tk.Label(container, text=small, font=("Segoe UI", 8), fg=style['muted'], bg=style['panel']).pack(pady=(2,0))
        buttons[k] = b
        ToolTip(b, f"Use the {label_txt} configuration ({small})")

    # Separator
    separator = tk.Frame(panel, bg='#2a3744', height=1)
    separator.pack(fill='x', padx=20, pady=(5, 8))

    # options row - DEBUG MODE HIDDEN (set DEBUG_MODE = True to show)
    DEBUG_MODE = False  # Change to True to enable debug checkbox
    opts = tk.Frame(panel, bg=style['panel'])
    if DEBUG_MODE:
        opts.pack(fill='x', padx=12, pady=(4,12))
    debug_mode_var = tk.BooleanVar()
    if DEBUG_MODE:
        chk = tk.Checkbutton(opts, text='Enable Debug Mode', variable=debug_mode_var, bg=style['panel'], fg=style['fg'], selectcolor=style['btn'], activebackground=style['panel'], activeforeground=style['accent'], font=("Segoe UI", 9), cursor='hand2', bd=0)
        chk.pack(side='left')
        ToolTip(chk, 'Show detection match score and debug overlay')

    # status + control with card style
    status_frame = tk.Frame(root, bg=style['bg'])
    status_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0,8))
    
    status_panel = tk.Frame(status_frame, bg=style['panel'], relief='flat', highlightthickness=1, highlightbackground='#2a3744')
    status_panel.pack(fill='x')
    
    status_label = tk.Label(status_panel, text='⚫ Ready', bg=style['panel'], fg=style['muted'], font=("Segoe UI", 10, 'bold'), pady=10)
    status_label.pack(side='left', padx=15)

    stop_button = tk.Button(status_panel, text='⏹ STOP TIMER', font=("Segoe UI", 10, 'bold'), bg=style['btn'], fg=style['muted'], activebackground=style['accent'], activeforeground='white', state='disabled', bd=0, width=13, cursor='hand2', relief='flat')
    stop_button.pack(side='right', padx=12, pady=8)

    # Spike Info Button (below stop button)
    def show_spike_info():
        info_win = tk.Toplevel(root)
        info_win.title("Spike Mechanics")
        info_win.geometry("420x365")
        info_win.configure(bg=style['bg'])
        info_win.resizable(False, False)
        info_win.lift()
        info_win.attributes('-topmost', True)
        
        title = tk.Label(info_win, text="⏱️ SPIKE MECHANICS", bg=style['bg'], fg=style['accent'], font=('Segoe UI Bold', 11))
        title.pack(pady=8)
        
        # Container
        container = tk.Frame(info_win, bg=style['bg'])
        container.pack(fill='both', expand=True, padx=12, pady=(0, 6))
        
        # Planting
        plant_frame = tk.Frame(container, bg=style['panel'], relief='ridge', bd=1)
        plant_frame.pack(fill='x', pady=2)
        tk.Label(plant_frame, text="🌱 PLANTING", bg=style['panel'], fg=style['accent'], font=('Segoe UI Bold', 9), anchor='w').pack(padx=8, pady=(4,2))
        tk.Label(plant_frame, text="• Takes 4 seconds", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=(0,4), anchor='w')
        
        # Detonation
        det_frame = tk.Frame(container, bg=style['panel'], relief='ridge', bd=1)
        det_frame.pack(fill='x', pady=2)
        tk.Label(det_frame, text="💣 DETONATION TIMER", bg=style['panel'], fg=style['accent'], font=('Segoe UI Bold', 9), anchor='w').pack(padx=8, pady=(4,2))
        tk.Label(det_frame, text="• 45 seconds - Consistent beeping", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=0, anchor='w')
        tk.Label(det_frame, text="• 20 seconds - Double beeping", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=0, anchor='w')
        tk.Label(det_frame, text="• 10 seconds - Triple beeping", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=0, anchor='w')
        tk.Label(det_frame, text="• 7 seconds - White sphere closes in", bg=style['panel'], fg=style['accent'], font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=(0,4), anchor='w')
        
        # Defusing
        def_frame = tk.Frame(container, bg=style['panel'], relief='ridge', bd=1)
        def_frame.pack(fill='x', pady=2)
        tk.Label(def_frame, text="🔧 DEFUSING", bg=style['panel'], fg=style['accent'], font=('Segoe UI Bold', 9), anchor='w').pack(padx=8, pady=(4,2))
        tk.Label(def_frame, text="• Takes 7 seconds total", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=(0,4), anchor='w')
        
        # Half defuse
        half_frame = tk.Frame(container, bg=style['panel'], relief='ridge', bd=1)
        half_frame.pack(fill='x', pady=2)
        tk.Label(half_frame, text="⚡ HALF DEFUSE CHECKPOINT", bg=style['panel'], fg='#ffa500', font=('Segoe UI Bold', 9), anchor='w').pack(padx=8, pady=(4,2))
        tk.Label(half_frame, text="• Activates at 3.5 seconds - Progress saved!", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=0, anchor='w')
        tk.Label(half_frame, text="• Outer casing falls to halfway", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=0, anchor='w')
        tk.Label(half_frame, text="• Audio changes to higher pitch", bg=style['panel'], fg='white', font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=0, anchor='w')
        tk.Label(half_frame, text="• If canceled, resets to 3.5s (not 0s)", bg=style['panel'], fg=style['accent'], font=('Segoe UI', 8), anchor='w').pack(padx=16, pady=(0,4), anchor='w')
        
        btn_close = tk.Button(info_win, text="Close", bg=style['btn'], fg=style['fg'], activebackground=style['btn_hover'], font=('Segoe UI', 9), relief='flat', cursor='hand2', command=info_win.destroy)
        btn_close.pack(pady=(4,8), padx=12, fill='x')

    info_btn_frame = tk.Frame(root, bg=style['bg'])
    info_btn_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=(0, 15))
    
    btn_spike_info = tk.Button(info_btn_frame, text='ℹ️ Info', bg='#2a3f5f', fg='white', activebackground='#3a5f7f', font=('Segoe UI', 9), relief='flat', cursor='hand2', command=show_spike_info, width=10, highlightthickness=1, highlightbackground='#1a2f4f')
    btn_spike_info.pack(side='left', padx=0, pady=0)
    ToolTip(btn_spike_info, "View Spike mechanics and timings")

    # keyboard shortcuts
    root.bind('<Escape>', lambda e: stop_detector() if stop_button['state']=='normal' else root.destroy())

    # --- Logic ---
    detector_thread = None

    def start_detector(selection):
        nonlocal detector_thread
        
        # Resolution mismatch warning
        screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
        res_map = {'1k': (1920, 1080), '2k': (2560, 1440), '4:3': (1440, 1080)}
        if (screen_w, screen_h) != res_map[selection]:
            msg = f"Warning: Your current screen is {screen_w}x{screen_h},\nbut you selected the configuration for {res_map[selection][0]}x{res_map[selection][1]}.\nThis may cause detection to fail. Continue anyway?"
            if not messagebox.askyesno("Resolution Mismatch", msg): return

        config = RESOLUTION_SETTINGS[selection]
        config['debug_mode'] = debug_mode_var.get()
        
        status_label.config(text="🟢 Running...", fg="#2ed573")
        for btn in buttons.values(): btn.config(state="disabled")
        stop_button.config(state="normal", bg='#ff4655', fg='white')
        print(f"Selected {config['description']} configuration, starting detection...")
        
        stop_event.clear()
        score_win = ScoreDisplay(root) if config['debug_mode'] else None
        countdown_win = CountdownTimer(root)
        
        # Show debug window and bring to front
        if score_win:
            score_win.deiconify()
            score_win.lift()
            score_win.attributes('-topmost', True)
            print(f"Debug window created at position: +{score_win.winfo_x()}+{score_win.winfo_y()}")

        detector_thread = threading.Thread(
            target=detector_thread_func, 
            args=(root, config, countdown_win, score_win),
            daemon=True
        )
        detector_thread.start()

    def stop_detector():
        global countdown_active
        print("Stopping timer...")
        stop_event.set()
        countdown_active = False  # Stop any active countdown
        status_label.config(text="⚫ Stopped", fg="#8a8a8a")
        for btn in buttons.values(): btn.config(state="normal")
        stop_button.config(state="disabled", bg='#2d3a45', fg='#8a8a8a')

    def show_window(icon=None, item=None):
        root.deiconify()
        root.lift()
        root.focus_force()

    def hide_window():
        root.withdraw()

    def quit_app(icon=None, item=None):
        if icon:
            icon.stop()
        stop_event.set()
        root.quit()
        sys.exit(0)

    def on_closing():
        # Hide to tray instead of closing
        hide_window()

    # System tray icon
    def create_tray_icon():
        # Load icon from file
        try:
            import os
            import sys
            
            # Get the correct path for icon (works for both script and exe)
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                application_path = sys._MEIPASS
            else:
                # Running as script
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, 'icon_ultra_sharp.ico')
            
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                print(f"System tray icon loaded from: {icon_path}")
            else:
                print(f"Icon file not found at: {icon_path}, using fallback")
                # Fallback: create simple icon if file not found
                image = Image.new('RGB', (64, 64), color='#ff4655')
                dc = ImageDraw.Draw(image)
                dc.rectangle([16, 16, 48, 48], fill='white')
        except Exception as e:
            print(f"Could not load icon_ultra_sharp.ico: {e}, using fallback icon")
            # Fallback: create simple icon
            image = Image.new('RGB', (64, 64), color='#ff4655')
            dc = ImageDraw.Draw(image)
            dc.rectangle([16, 16, 48, 48], fill='white')
        
        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem('Show', show_window, default=True),
            pystray.MenuItem('Exit', quit_app)
        )
        
        icon = pystray.Icon('ValTimer', image, 'Valorant Spike Timer', menu)
        return icon

    # Start tray icon in separate thread
    tray_icon = create_tray_icon()
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()

    # --- Command and Event Binding ---
    for res, btn in buttons.items():
        btn.config(command=lambda r=res: start_detector(r))
    stop_button.config(command=stop_detector)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f'+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()