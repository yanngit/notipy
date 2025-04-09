#!/bin/bash

# exit script if a command fails
set -e

# Your program name
program_name=notipy

# Full path to your python interpreter
# you may get this by typing which python in your terminal
python_path=$(which python3.10)

# Full path to the source directory
source_dir=$(pwd)

# Full path to your python script
script_path=$source_dir/$program_name.py

echo "[Unit]
Description=Notipy - never miss your meetings
After=network.target

[Service]
ExecStart=$python_path $script_path
WorkingDirectory=$source_dir
StandardOutput=inherit
StandardError=inherit
Restart=always

[Install]
WantedBy=graphical-session.target" | sudo tee /etc/systemd/user/$program_name.service