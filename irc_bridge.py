import asyncio
import ssl
import re
import logging
import argparse
from threading import Thread
from colorama import Fore, Style, init
from rstr import xeger
from pyrogram import Client

# Constants
DEFAULT_CONFIG_FILE = "config.json"

# Initialize colorama for colored console output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="irc_bot.log",
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Define loggers for different components
irc_logger = logging.getLogger("irc")
telegram_logger = logging.getLogger("telegram")

# IRC Server and Channel Configuration
irc_server = None
irc_channels = []

# Initialize the Pyrogram client for Telegram bot
app = Client("YourBotSession", api_id=YOUR_API_ID, api_hash="YOUR_API_HASH")

# Function to configure IRC server and channels dynamically
def configure_irc():
    global irc_server, irc_channels
    irc_server = args.server
    irc_channels = args.channels.split(",")

# Initialize the IRC connection
async def initialize_irc(nick, user):
    while True:
        try:
            reader, writer = await async_irc_connect(nick, user)
            logger.info("Connected to IRC server: %s", irc_server)

            for channel in irc_channels:
                writer.write(f"JOIN {channel}".encode("utf-8") + b"\r\n")
                await writer.drain()
                irc_logger.info("Joined IRC channel: %s", channel)

            await read_irc_messages(reader, writer)
        except Exception as e:
            logger.error("Error connecting to IRC server: %s", e)
            await asyncio.sleep(60)  # Retry after a minute

# Function to read IRC messages
async def read_irc_messages(reader, writer):
    while not reader.at_eof():
        try:
            data = await reader.readline()
            data = data.decode("utf-8", "ignore").split(" ")

            if data[0] == "PING":
                logger.debug("Received PING: %s", data[1].strip())
                writer.write(f"PONG {data[1].strip()}".encode("utf-8") + b"\r\n")
                await writer.drain()
                irc_logger.debug("Sent PONG response")
            else:
                message_handler(data)
        except Exception as e:
            logger.error("Read loop error: %s", e)

# Function to handle IRC connection asynchronously
async def async_irc_connect(nick, user):
    try:
        sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        sc.check_hostname = False
        sc.verify_mode = ssl.CERT_NONE
        reader, writer = await asyncio.open_connection(irc_server, args.port, ssl=sc)
    except Exception as e:
        logger.error("Error connecting to IRC server: %s", e)
        raise e

    await writer.drain()
    writer.write(f"NICK {nick}".encode("utf-8") + b"\r\n")
    await writer.drain()
    writer.write(f"USER {user} {user} {user} :{user}".encode("utf-8") + b"\r\n")

    return reader, writer

# Function to handle incoming messages
def message_handler(data):
    if data[1] == "PRIVMSG":
        message = " ".join(data[3:])[1:]
        matches = to_match_regex.findall(message)
        if matches:
            for match in matches:
                send_to_telegram(f"irc_message: {match}")

# Function to send messages to Telegram
def send_to_telegram(message):
    try:
        app.send_message(chat_id=args.telegram_channel_id, text=message)
        telegram_logger.info("Sent message to Telegram: %s", message)
    except Exception as e:
        logger.error("Error sending message to Telegram: %s", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRC to Telegram Bridge")
    parser.add_argument("--server", required=True, help="IRC server address")
    parser.add_argument("--channels", required=True, help="IRC channels (comma-separated)")
    parser.add_argument("--port", type=int, default=6667, help="IRC server port")
    parser.add_argument("--telegram_channel_id", required=True, help="Telegram channel ID")
    args = parser.parse_args()

    # Start IRC connection and message handling in a separate thread
    nick = xeger(r"[A-Z]{4,6}[1-9]{3,4}")
    user = nick.lower()
    Thread(target=initialize_irc, args=(nick, user), daemon=True).start()

    # Start the Pyrogram client for Telegram
    app.run()
