import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "").split(",")]
PRIVATE_CHANNEL_ID = "@YourPrivateChannel"  # замените на ваш канал
