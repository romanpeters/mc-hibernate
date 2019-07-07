# Minecraft Start-Stop

Automatically start your Minecraft server when someone tries to join and shut it down when no one is online anymore.

1.) Edit `config.py`
1.) Run `run.py`

The script needs to run on the same host and port as the Minecraft server in order to listen for joining players.

I'm using it in conjunction with a Minecraft server in a Docker container ([itzg/minecraft-server](https://hub.docker.com/r/itzg/minecraft-server/)), you might be able to use it with other type of servers by editing `config.py`, but ymmv.

