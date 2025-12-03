import subprocess
import tkinter as tk
import time
import threading


def get_mouse_position():
    # Use xdotool to get the current mouse position
    result = subprocess.run("xdotool getmouselocation --shell", shell=True, capture_output=True, text=True)
    position = {}
    for line in result.stdout.splitlines():
        key, value = line.split('=')
        position[key] = int(value)
    return position['X'], position['Y']

def shake_window(win, amplitude=10, shakes=8, speed=30):
    """Wizz animation: horizontally shake the window."""
    x = win.winfo_x()
    y = win.winfo_y()

    for _ in range(shakes):
        win.geometry(f"+{x + amplitude}+{y}")
        win.update()
        time.sleep(speed/1000)

        win.geometry(f"+{x - amplitude}+{y}")
        win.update()
        time.sleep(speed/1000)

    win.geometry(f"+{x}+{y}")  # Reset position


def fade_in(win, steps=15, delay=25):
    """Fade-in animation."""
    for i in range(steps):
        alpha = i / steps
        win.attributes("-alpha", alpha)
        win.update()
        time.sleep(delay/1000)
    win.attributes("-alpha", 1.0)


def create_rainbow_background(canvas, width, height):
    """Draw horizontal rainbow stripes."""
    colors = ["#FF0000", "#FF7F00", "#FFFF00",
              "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]

    stripe_height = height // len(colors)

    for i, color in enumerate(colors):
        canvas.create_rectangle(
            0, i * stripe_height,
            width, (i + 1) * stripe_height,
            fill=color, outline=color
        )


def show_alert(event_summary, event_start, html_link):
    # --- window creation ---
    width, height = 500, 200
    x_pos, y_pos = get_mouse_position()

    root = tk.Tk()
    root.title("Meeting Reminder")
    root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.0)  # start invisible for fade-in

    # --- rainbow background ---
    canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
    canvas.place(x=0, y=0)
    create_rainbow_background(canvas, width, height)

    # --- Text + Buttons ---
    frame = tk.Frame(root, bg="#ffffff80")  # translucent frame
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label_text = f"Upcoming: {event_summary}\nat {event_start.strftime('%H:%M')}"
    label = tk.Label(frame, text=label_text, font=("Arial", 14), bg="#ffffff80")
    label.pack(pady=10)

    close_button = tk.Button(frame, text="Close", command=root.destroy)
    close_button.pack(pady=5)

    if html_link:
        go_to = tk.Button(frame, text="Go to meet", command=lambda: go_to_meet(html_link, root))
        go_to.pack(pady=5)

    # --- run animations in a separate thread ---
    def animate():
        fade_in(root)
        shake_window(root)  # wizz effect

    threading.Thread(target=animate, daemon=True).start()

    root.mainloop()