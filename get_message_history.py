
from telethon import TelegramClient
from decouple import config
import json
import asyncio
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")

async def main(client):
    messages = []
    async for message in client.iter_messages(-1001286966173, limit=1100):
      messages.append({  
        'text': message.text,
        'date': message.date.isoformat()
      })
    messages.reverse()
    with open('export.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

FROM = [int(i) for i in FROM_.split()]

async def main_wrapper():
    async with TelegramClient(SESSION, APP_ID, API_HASH) as client:
        await main(client)
 
asyncio.run(main_wrapper())