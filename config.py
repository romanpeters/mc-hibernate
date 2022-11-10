import logging

LOGGING = logging.DEBUG

HOST = "127.0.0.1"
PORT = 25565

# Time in seconds to wait for the port to become available
STARTUP_DELAY = 1
SHUTDOWN_DELAY = 40

# Time to wait for the player to join
STARTUP_TIMER = 180

# Time to wait for the server being empty
SHUTDOWN_TIMER = 300

# Change the motd to the start time
EDIT_MOTD = True
SERVER_PROPERTIES = "/root/minecraft/server.properties"
