import subprocess
import tkinter as tk

def go_to_meet(link, root):
    subprocess.run(["xdg-open", link])
    root.destroy()

def show_alert(event_summary, event_start, html_link):
    x_pos, y_pos = get_mouse_position()
    root = tk.Tk()
    root.title("Meeting in a few minutes")
    root.geometry(f"500x200+{x_pos}+{y_pos}")
    label_text = f"Upcoming: {event_summary}\nat {event_start.strftime('%H:%M')}"
    label = tk.Label(root, text=label_text)
    label.pack(pady=10)

    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)
    if html_link != '':
        go_to = tk.Button(root, text=f"Go to meet ", command=lambda: go_to_meet(html_link, root))
        go_to.pack(pady=10)
    root.attributes('-topmost', True)
    root.mainloop()

def get_mouse_position():
    # Use xdotool to get the current mouse position
    result = subprocess.run("xdotool getmouselocation --shell", shell=True, capture_output=True, text=True)
    position = {}
    for line in result.stdout.splitlines():
        key, value = line.split('=')
        position[key] = int(value)
    return position['X'], position['Y']