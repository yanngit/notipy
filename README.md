# Notifier
## Linux only
Available only for linux, install pre-requisite for your system with: 
```shell
sudo apt-get update
sudo apt-get install -y libgl1-mesa-dev xorg-dev libxcursor-dev libxrandr-dev libxinerama-dev libxi-dev pkg-config
```
Go 1.22 is needed.
## Build
`go build -o notify`
## Run
`./notify`