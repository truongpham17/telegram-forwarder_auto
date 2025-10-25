from telethon import TelegramClient
from decouple import config
import requests
import logging
import asyncio

logging.basicConfig(
    format='[%(levelname)5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)

PORTS = [3000]

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = int(config("FROM_CHANNEL"))  # e.g. -1001252615519

try:
    client = TelegramClient(SESSION, APP_ID, API_HASH)
    client.start()  # sync start is fine outside asyncio
except Exception as ap:
    print(f"ERROR - {ap}", flush=True)
    exit(1)

# (Optional) Show channel info once
channel = client.loop.run_until_complete(client.get_entity(FROM_))
print(f"Title: {getattr(channel, 'title', channel)}", flush=True)
print(f"ID: {getattr(channel, 'id', None)}", flush=True)

def post_to_local(message: str):
      url = f'http://localhost:3000/signal'
      try:
          requests.post(url, json={'message': message or ""}, timeout=5)
      except Exception as e:
          print(f"[POST ERROR] {e}", flush=True)

async def poll_latest(channel_id: int, interval_sec: int = 3):
    # prime last_id with current latest
    last_id = 0
    print(f"[POLL] start channel={channel_id} last_id={last_id}", flush=True)

    while True:
        try:
            msgs = await client.get_messages(channel_id, limit=1)
            if msgs:
                m = msgs[0]
                if m.id > last_id:
                    text = m.text or getattr(m, "message", "") or ""
                    post_to_local(text)
                    last_id = m.id
        except Exception as e:
            print(f"[POLL ERROR] {e}", flush=True)

        await asyncio.sleep(interval_sec)

# Run the polling loop on Telethon's loop
client.loop.run_until_complete(poll_latest(FROM_))
