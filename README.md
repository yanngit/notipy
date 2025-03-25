# Notifier

## Pre requisite
Available only for linux, install pre-requisite for your system with: 
```shell
sudo apt-get update
sudo apt-get install -y python3.10-tk xdotool
```
Python 3.10 is needed with at least these packages to install: 
```bash 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Google calendar authent
Get a *credentials.json* file for OAUTH API connexion. Follow [this](https://developers.google.com/calendar/api/quickstart/python) 
tutorial if you're new to GCP. The program is expecting the file to be named `credentials.json` so rename it after 
download to match this exact name.

## Configure
Update the notipy.py file by changing the calendar values:
``` python
schedule = {
        'Monday': [(9, 14), (9, 24), (9, 58), (13, 58), (15,28)],
        'Tuesday': [(9, 14), (9, 24), (15, 0)],
        'Wednesday': [(9, 14), (9, 24),(11, 50)],
        'Thursday': [(9, 14), (9, 24), (14,13), (16,58)],
        'Friday': [(9, 58)],
        'Saturday': [],
        'Sunday': [],
    }
```
Once done you can save the file and run the app.

## Running the app 
sudo python notipy.py

## Stop the app
The app is running as a daemon so to find it you can: 
`ps -aux | grep notipy` and then `kill -9 NOTIPY_PID`




