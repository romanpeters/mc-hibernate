"""
This script automatically starts and stops a Minecraft server.
If someone tries to join the server is started.
If no players are online anymore the server is stopped.
"""
import socket
import time
import subprocess
import logging
import sys
import fileinput
import config


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def start_server():
    command = config.START_COMMAND
    subprocess.run(command.split())
    logger.info("Started server")

def stop_server():
    command = config.STOP_COMMAND
    try:
        subprocess.check_output(command.split())
    except subprocess.CalledProcessError:
        logger.warn(f"Failed to stop server, assuming Minecraft is not running")
    logger.info("Stopped server")

def players_online() -> bool:
    """Check if there are any players online"""
    command = config.MCSTATUS_COMMAND
    try:
        status = subprocess.check_output(command.split())
    except subprocess.CalledProcessError:
        logger.warn(f"Failed to check mcstatus, assuming Minecraft is not running")
        return False
    else:
        if "players: 0" in str(status):
            return False
    return True

def wait_for_connection():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((config.HOST, config.PORT))
    serversocket.listen(5)

    logger.info("Waiting for connection...")
    (clientsocket, address) = serversocket.accept()

    logger.info(f"Got a connection from {address}")

    clientsocket.send("Server is starting".encode("utf-8"))

    logger.debug("Closing sockets")
    clientsocket.close()
    serversocket.close()


def wait_for_empty_server():
    while players_online():
        logger.debug(f"Minecraft Server is active, sleeping for f{config.SHUTDOWN_TIMER} seconds")
        time.sleep(config.SHUTDOWN_TIMER)
    logger.debug("Minecraft Server is not active")

def edit_motd():
    for line in fileinput.input("server.properties", inplace=True):
        if "motd=" in line:
            sys.stdout.write(f"motd=Server started at {time.strftime('%H:%M')}")


if __name__=="__main__":

    # Start the main flow
    while True:
        wait_for_empty_server()
        sys.stdout.flush()  # show log in systemd service

        stop_server()
        sys.stdout.flush()

        wait_for_connection()
        sys.stdout.flush()

        logger.debug(f"Wait {config.STARTUP_DELAY} second for the port to become available")
        time.sleep(config.STARTUP_DELAY)

        if config.EDIT_MOTD:
            logger.debug("Editing motd")
            edit_motd()

        start_server()
        sys.stdout.flush()

        logger.debug(f"Wait {config.STARTUP_TIMER} seconds for the player to join")
        time.sleep(cobfig.STARTUP_TIMER)
