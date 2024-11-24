#    Copyright (c) 2021 Ayush
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License > .

from telethon import TelegramClient, events
from decouple import config
import requests
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)


PORTS = [3001]
print('come here')

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")

FROM = [int(i) for i in FROM_.split()]
try:
    client = TelegramClient(SESSION, APP_ID, API_HASH)
    client.start()
    
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)


@client.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    try:
        # await client.send_message('@trading_signal_bot', event.message)
        message = event.message.text or event.message.caption
        for port in PORTS:
            url = 'http://localhost:' + str(port) + '/signal'
            data = {
                'message': message
            }
            
            try:
                requests.post(url, json=data)
            except Exception as inner_e:
                print(inner_e)
    except Exception as e:
        print(e)

print("Bot has started.")
client.run_until_disconnected()
