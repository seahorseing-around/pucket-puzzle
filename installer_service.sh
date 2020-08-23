#!/bin/sh

#Add service file & relead systemctl
echo "Copy in Service file"
cp game_time.service /lib/systemd/system/game_time.service
echo "Reload Systemd Daemon"
systemctl daemon-reload
#auto-start on startup
echo "Enable game_time service to autostart on startup"
systemctl enable game_time
#start & check status
echo "Start game_time service"
sudo service game_time start
sudo service game_time status
