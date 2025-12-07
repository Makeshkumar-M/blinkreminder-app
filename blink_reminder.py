# ---------------------------------------------------------------
# Blink Reminder App
# Reminds users to blink and rest their eyes at regular intervals.
# Features:
#   - Animated GIF popup with eye-care tips
#   - Snooze and auto-close options
#   - Gentle sound alert
#   - System tray integration (pause/resume/exit)
# ---------------------------------------------------------------
import tkinter as tk
import random
from threading import Thread
import sys
import winsound
from pystray import Icon, Menu, MenuItem

# ---------------- Settings ----------------
GIF_PATH = r"C:\Python Projects\eye_blink.gif"  # Animated GIF
ICON_PATH = r"C:\Python Projects\icon.ico"      # Tray icon (must be .ico)

REMINDER_INTERVAL = 20 * 60 * 1000 # 20 minutes in ms
SNOOZE_INTERVAL =  5 * 60 * 1000  # 5 minutes in ms
AUTO_CLOSE_TIME = 5000             # 5 seconds in ms

TIPS = [
    "Blink 10 times quickly.",
    "Look away from the screen for 20 seconds.",
    "Rotate your eyes clockwise and counterclockwise.",
    "Focus on a distant object for 15 seconds.",
    "Close your eyes and take a deep breath."
]

# ---------------- Reminder Popup ----------------
def show_reminder():
    reminder = tk.Toplevel(root)
    reminder.title("Blink Reminder")
    reminder.resizable(False, False)

    # Popup size
    win_w, win_h = 300, 200
    reminder.geometry(f"{win_w}x{win_h}")

    # Position bottom-right
    screen_w = reminder.winfo_screenwidth()
    screen_h = reminder.winfo_screenheight()
    x = screen_w - win_w - 20
    y = screen_h - win_h - 60
    reminder.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # Load GIF frames (native Tkinter)
    frames = []
    try:
        for i in range(50):  # adjust if GIF has more frames
            frames.append(tk.PhotoImage(file=GIF_PATH, format=f"gif - {i}"))
    except tk.TclError:
        pass
    frame_count = len(frames)

    label = tk.Label(reminder)
    label.pack(pady=5)

    def animate(counter=0):
        frame = frames[counter]
        counter = (counter + 1) % frame_count
        label.configure(image=frame)
        reminder.after(100, animate, counter)

    animate()

    # Random eye-care tip
    message = tk.Label(
        reminder,
        text="Time to blink your eyes!\n" + random.choice(TIPS),
        font=("Arial", 11)
    )
    message.pack(pady=5)

    # Buttons
    btn_ok = tk.Button(reminder, text="OK", command=reminder.destroy)
    btn_ok.pack(side="left", expand=True, padx=10, pady=5)

    def snooze():
        reminder.destroy()
        root.after(SNOOZE_INTERVAL, show_reminder)

    btn_snooze = tk.Button(reminder, text="Snooze 5 min", command=snooze)
    btn_snooze.pack(side="right", expand=True, padx=10, pady=5)

    # Auto close after 10 sec
    reminder.after(AUTO_CLOSE_TIME, reminder.destroy)

    # Gentle sound alert
    winsound.MessageBeep()

    # Schedule next reminder
    root.after(REMINDER_INTERVAL, show_reminder)


# ---------------- System Tray ----------------
def run_tray():
    icon = Icon(
        "BlinkReminder",
        ICON_PATH,
        menu=Menu(
            MenuItem("Resume", lambda: root.after(1000, show_reminder)),
            MenuItem("Pause", lambda: None),  # extend later
            MenuItem("Exit", lambda: (icon.stop(), root.quit(), sys.exit()))
        )
    )
    icon.run()


# ---------------- Main App ----------------
root = tk.Tk()
root.withdraw()  # Hide root window

# Start first reminder
root.after(1000, show_reminder)

# Run tray icon in background thread
Thread(target=run_tray, daemon=True).start()

root.mainloop()
