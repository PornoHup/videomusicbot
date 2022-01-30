import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Video Stream")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "Ruhsuzbeyyy")
ALIVE_NAME = getenv("ALIVE_NAME", "Ruhsuzbeyyy")
BOT_USERNAME = getenv("BOT_USERNAME", "veezvideobot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "cleo_invida")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "@ruhsuzbeyyy")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "ruhsuzbeyyy")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/Logo-01-30-2")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://t.me/ruhsuzbeyyy")
IMG_1 = getenv("IMG_1", "https://telegra.ph/Logo-01-30-2")
IMG_2 = getenv("IMG_2", "https://telegra.ph/Logo-01-30-2")
IMG_3 = getenv("IMG_3", "https://telegra.ph/Logo-01-30-2")
