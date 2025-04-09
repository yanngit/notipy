#!/bin/bash

# exit script if a command fails
set -e

# Your program name
program_name=notipy

# Full path to your python interpreter
# you may get this by typing which python in your terminal
python_path=/usr/bin/python3.10

# Full path to the source directory
source_dir=$(pwd)

# Full path to your python script
script_path=$source_dir/$program_name.py

user=$(whoami)

echo "[Unit]
Description=A python notifier to never miss your meetings

[Service]
ExecStart=$python_path $script_path
WorkingDirectory=$source_dir
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$user

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/$program_name.service