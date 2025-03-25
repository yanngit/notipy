import subprocess
import tkinter as tk
import datetime
import time
import os
import signal
import sys

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
    label = tk.Label(root, text="You have a scheduled event!")
    label.pack(pady=10)

    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)

    root.attributes('-topmost', True)  # Set the window on top
    root.mainloop()

def match_schedule(day_of_week, current_hour, current_minute):
    schedule = {
        'Monday': [(9, 14), (9, 29), (9, 58), (13, 58), (15,28)],
        'Tuesday': [(9, 14), (9, 29), (14, 14)],
        'Wednesday': [(9, 14), (9, 29),(11, 50)],
        'Thursday': [(9, 14), (9, 29), (14,13), (16,58)],
        'Friday': [(9, 58)],
        'Saturday': [],
        'Sunday': [],
    }

    times = schedule.get(day_of_week, [])
    return (current_hour, current_minute) in times

def daemon_run():
    while True:
        now = datetime.datetime.now()
        current_day = now.strftime("%A")  # Get the day of the week
        current_hour = now.hour
        current_minute = now.minute

        if match_schedule(current_day, current_hour, current_minute):
            show_alert()
            time.sleep(60)  # Wait a minute to prevent multiple alerts in the same minute
        else:
            time.sleep(30)  # Check every 30 seconds

def become_daemon():
    # Fork the process to run in the background
    if os.fork():
        sys.exit(0)
    os.setsid()
    if os.fork():
        sys.exit(0)
    # Redirect standard file descriptors
    stdout='/var/log/notipy_out.log'
    stderr='/var/log/notipy_err.log'
    # stdin
    with open('/dev/null', 'r') as dev_null:
        os.dup2(dev_null.fileno(), sys.stdin.fileno())
    # stderr - do this before stdout so that errors about setting stdout write to the log file.
    #
    # Exceptions raised after this point will be written to the log file.
    sys.stderr.flush()
    with open(stderr, 'a+') as stderr:
        os.dup2(stderr.fileno(), sys.stderr.fileno())
    # stdout
    #
    # Print statements after this step will not work. Use sys.stdout
    # instead.
    sys.stdout.flush()
    with open(stdout, 'a+') as stdout:
        os.dup2(stdout.fileno(), sys.stdout.fileno())

    # Ignore signals that can kill the daemon
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

if __name__ == "__main__":
    become_daemon()
    daemon_run()