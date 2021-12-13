# IP Cam Display



## Getting started

Git clone this repository
```
git clone https://gitlab.com/AndrewSkea/ipcamdisplay.git
cd ipcamdisplay
```

## Update your camera settings

Update the constants.py with your camera settings and ceck the get_urls function to ensure the right rtsp streams are getting formed

## Install as a service

This will copy this directory into a /etc/ dir and ru from there using the main python3 installed

If you want to use a different python version, update it in the deploy/ipcamdisplay.service file

If you want update any files and re-install, re-do these steps below from the root directory:

```
sudo cp -fR src /etc/ipcamdisplay
sudo cp -fR deploy/ipcamdisplay.service /etc/systemd/system/ipcamdisplay.service
sudo systemctl daemon-reload
sudo systemctl enable ipcamdisplay.service
sudo systemctl start ipcamdisplay.service
```

