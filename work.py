from telethon import TelegramClient, events
from decouple import config
import requests

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = int(config("FROM_CHANNEL"))
TO_ = config("TO_CHANNEL")

client = TelegramClient(SESSION, APP_ID, API_HASH)
NODE_ENDPOINT = 'http://localhost:3000/trade-signal'

@client.on(events.NewMessage(incoming=True, chats=FROM_))
async def handler(event):
    message = event.message.message
    print("Forwarding message:", message)

    try:
        requests.post(NODE_ENDPOINT, json={"message": message})
    except Exception as e:
        print("Error forwarding:", e)
    await client.send_message(TO_, event.message)

print("Bot is running...")
client.start()
client.run_until_disconnected()