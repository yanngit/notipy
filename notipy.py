import subprocess
import datetime
import time
import os
import signal
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ui import show_alert

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
creds = None
last_token_refresh = 0

def get_tokens():
    global creds, last_token_refresh
    current_time = time.time()
    # Check if the token was refreshed within the last hour (3600 seconds)
    if current_time - last_token_refresh < 3600:
        print("Token refresh skipped, last refresh was less than an hour ago.")
        return

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(host='127.0.0.1',port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

def get_next_upcoming_event():
    global creds
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the next upcoming event")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=3,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return None

        for event in events:
            event_summary = event.get('summary', 'No Title')
            start_time_str = event['start'].get('dateTime', event['start'].get('date'))
            event_start_time = datetime.datetime.fromisoformat(start_time_str)
            if is_event_already_started(event_start_time):
                print(f"Event [{event_summary}] on [{event_start_time}] already started, watching next event")
                continue
            print(f"Next valid event is [{event_summary}] on [{event_start_time}]")
            return event

    except HttpError as error:
        print(f"An error occurred: {error}")

# Utility function to check time difference
def is_event_in_minutes(event_datetime, minutes=2):
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = event_datetime.astimezone(tz=datetime.timezone.utc) - now
    return 0 <= delta.total_seconds() <= minutes * 60

def is_event_already_started(event_datetime):
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = event_datetime.astimezone(tz=datetime.timezone.utc) - now
    return 0 > delta.total_seconds()

def go_to_meet(link, root):
    subprocess.run(["xdg-open", link])
    root.destroy()

def daemon_run():
    while True:
        get_tokens()
        event = get_next_upcoming_event()
        if event:
            event_summary = event.get('summary', 'No Title')
            start_time_str = event['start'].get('dateTime', event['start'].get('date'))
            event_link = event.get('hangoutLink', '')

            # Parse event start into datetime object
            event_start_time = datetime.datetime.fromisoformat(start_time_str)
            if event_start_time.tzinfo is None:
                event_start_time = event_start_time.replace(tzinfo=datetime.timezone.utc)

            # Check if the event is in less than 2 minutes from now
            if is_event_in_minutes(event_start_time, minutes=1):
                print('event is close, showing an alert')
                show_alert(event_summary, event_start_time, event_link)
                # Wait for 2 min and 1 second to avoid multiple alerts for one event
                time.sleep(121)
                continue
        # If no event is soon or there were no events, wait 30 seconds then check again
        print ('event is too far, sleeping and back in the loop')
        time.sleep(30)


def become_daemon():
    # Fork the process to run in the background
    if os.fork():
        sys.exit(0)
    os.setsid()
    if os.fork():
        sys.exit(0)
    # Redirect standard file descriptors
    stdout='./notipy_out.log'
    stderr='./notipy_err.log'
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
    # become_daemon()
    daemon_run()