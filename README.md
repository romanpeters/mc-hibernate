# Minecraft Hibernate

Automatically start your Minecraft server when someone tries to join and shut it down when no one is online anymore.  

This script spawns a service on the same port as the Minecraft server to listen for incoming connections and needs to run on the same host.
When a player tries to connect (read: loads Minecraft's multiplayer screen, containing this server), the script automatically starts the Minecraft server, which allows the player to connect after some seconds.

1) Edit `START.sh.example` and rename it to `START.sh`
1) Edit `STOP.sh.example` and rename it to `STOP.sh`
1) Make the .sh files executable: `chmod +x START.sh STOP.sh`
1) `python3 run.py`

### START.sh
This script should contain the command to start your server. For example `docker start minecraft` or `systemctl start minecraft.service`.
You can also add a notification service command here, for example using https://ntfy.sh.

### STOP.sh
This script should contain the command to stop your server.

### config.py
You can edit some settings here, such as the server address and the time-out before the server is shutdown.

# Systemd
In order to run Minecraft Hibernate at boot on Linux, create a file `/etc/systemd/system/mc-hibernate.service` containing:
```
[Unit]
Description=Minecraft Hibernate
After=network.target

[Service]
WorkingDirectory=/path/to/minecraft-hibernate
ExecStart=/usr/bin/python3 run.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Then run:  
```
$ systemctl daemon-reload
$ systemctl enable mc-hibernate
$ systemctl start mc-hibernate
```
