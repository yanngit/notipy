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
tutorial if you're new to GCP. The program is expecting the file to be named `credentials.json` in the root folder, so rename it after 
download to match this exact name.

## Running the app 
python3.10 notipy.py

## Stop the app
The app is running as a daemon so to find it you can: 
`ps -aux | grep notipy` and then `kill -9 NOTIPY_PID`

## Run the app as a service
You can install *notipy* as a linux service by running the `./install-service.sh` command.
Once installed you can : 
```bash
systemctl --user daemon-reload
systemctl --user enable notipy
systemctl --user status notipy
```

And verify everything is working fine.





