import subprocess
import tkinter as tk

def get_mouse_position():
    # Use xdotool to get the current mouse position
    result = subprocess.run("xdotool getmouselocation --shell", shell=True, capture_output=True, text=True)
    position = {}
    for line in result.stdout.splitlines():
        key, value = line.split('=')
        position[key] = int(value)
    return position['X'], position['Y']

def show_alert():
    x_pos, y_pos = get_mouse_position()

    root = tk.Tk()
    root.title("Alert")

    # Position the window at the mouse cursor location
    root.geometry(f"300x100+{x_pos}+{y_pos}")

    # Create an alert message and a close button
    label = tk.Label(root, text="This is a notification!")
    label.pack(pady=10)

    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)

    root.attributes('-topmost', True)  # Make sure the window appears on top
    root.mainloop()

if __name__ == "__main__":
    show_alert()