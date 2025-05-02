from telethon import TelegramClient, events
from decouple import config


APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")

client = TelegramClient(SESSION, APP_ID, API_HASH)

async def handler(event):
    # Forward message to your bot chat
    await client.send_message(TO_, event.message)

print("Bot is running...")
client.start()
client.run_until_disconnected()

