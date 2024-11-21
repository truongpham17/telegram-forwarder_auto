from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

from decouple import config
BOT_TOKEN = config("TELE_BOT_TOKEN")

PORTS = [3000, 3001]

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('come here')
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if(text.startswith('..')):
      for port in PORTS:
            url = 'http://localhost:' + str(port) + '/signal'
            data = {
                'message': text
            }
            try:
                requests.post(url, json=data)
            except Exception as inner_e:
                print(inner_e)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()