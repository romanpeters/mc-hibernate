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
import mcstatus


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

server = mcstatus.JavaServer.lookup(f"{config.HOST}:{config.PORT}")


def start_server():
    subprocess.call("./START.sh")
    logger.info("Started server")


def stop_server():
    try:
        subprocess.call("./STOP.sh")
    except subprocess.CalledProcessError as e:
        logger.warning(e)  # already stopped?
    logger.info("Stopped server")


def server_status() -> int:
    try:
        status = server.status()
        logger.info(f"{status.players.online} players online")
        return status.players.online
    except Exception as e:
        logger.warning(e)
        logger.warning(f"Failed to check mcstatus, assuming Minecraft is not running")
        return -1


def wait_for_connection():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("0.0.0.0", config.PORT))
    serversocket.listen(5)

    logger.info("Waiting for connection...")
    (clientsocket, address) = serversocket.accept()

    logger.info(f"Got a connection from {address}")

    clientsocket.send("Server is starting".encode("utf-8"))

    logger.debug("Closing sockets")
    clientsocket.close()
    serversocket.close()


def wait_for_empty_server():
    while server_status() > 0:
        logger.debug(
            f"Minecraft Server is active, sleeping for {config.SHUTDOWN_TIMER} seconds"
        )
        time.sleep(config.SHUTDOWN_TIMER)
    logger.debug("Minecraft Server is not active")


def edit_motd():
    for line in fileinput.input(config.SERVER_PROPERTIES, inplace=True):
        if "motd=" in line:
            sys.stdout.write(f"motd=Server started at {time.strftime('%H:%M')}")


if __name__ == "__main__":

    # Start the main flow
    while True:
        status = server_status()
        sys.stdout.flush()  # show log in systemd service

        if status == 0:
            stop_server()
            sys.stdout.flush()
        elif status > 0:
            logger.debug(
                f"Minecraft Server is active, sleeping for {config.SHUTDOWN_TIMER} seconds"
            )
            sys.stdout.flush()
            time.sleep(config.SHUTDOWN_TIMER)

            wait_for_empty_server()
            sys.stdout.flush()

        wait_for_connection()
        sys.stdout.flush()

        logger.debug(
            f"Wait {config.STARTUP_DELAY} seconds for the port to become available"
        )
        time.sleep(config.STARTUP_DELAY)

        if config.EDIT_MOTD:
            logger.debug("Editing motd")
            edit_motd()

        start_server()
        sys.stdout.flush()

        logger.debug(f"Wait {config.STARTUP_TIMER} seconds for the player to join")
        time.sleep(config.STARTUP_TIMER)
