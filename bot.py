from telethon import TelegramClient, events
from decouple import config
import requests
import logging

logging.basicConfig(
    format='[%(levelname)5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)


PORTS = [3000]

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = int(config("FROM_CHANNEL"))

try:
    client = TelegramClient(SESSION, APP_ID, API_HASH)
    client.start()
    
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)
    
channel = client.loop.run_until_complete(client.get_entity(FROM_))
print(f"Title: {channel.title}")
print(f"ID: {channel.id}")


@client.on(events.NewMessage())
async def sender_bH(event):
    try:
        # await client.send_message('@trading_signal_bot', event.message)
        message = event.message.text or event.message.caption
        for port in PORTS:
            url = 'http://localhost:' + str(port) + '/signal'
            print(message)
            data = {
                'message': message
            }
            try:
                requests.post(url, json=data)
            except Exception as inner_e:
                print(inner_e)
    except Exception as e:
        print(e)

# print("Bot has started.")
client.run_until_disconnected()