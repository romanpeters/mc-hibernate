HOST = "127.0.0.1"
PORT = 1337

COMMAND_START = "docker start minecraft-server"
COMMAND_STOP = "docker stop minecraft-server"
MCSTATUS_COMMAND = "docker exec minecraft-server mcstatus localhost status"

# Time to wait for the port to become available
STARTUP_DELAY = 1

# Time to wait for the player to join
STARTUP_TIMER = 90

# Time to wait for the server being empty
SHUTDOWN_TIMER = 300

# Change the motd to the start time
EDIT_MOTD = False
