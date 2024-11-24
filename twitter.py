from tweety import TwitterAsync
from tweety.filters import SearchFilters
import asyncio
from decouple import config
from telegram import Bot
import requests

USER = config("TWITTER_USER")
PASS = config("TWITTER_PASS")
SEARCH_TERM = "from:CryptoBheem"
INTERVAL = 5 * 60
BOT_TOKEN = config("TWITTER_TELE_BOT_TOKEN")
CHAT_ID=config("CHAT_ID")

PORT=3000

tele_bot = Bot(BOT_TOKEN)

async def main():
    app = TwitterAsync("session")
    await app.sign_in(USER, PASS)

    last_tweet_ids = []

    while True:
        all_tweets = await app.search(SEARCH_TERM, filter_= SearchFilters.Latest)
        current_tweet_ids = [tweet.id for tweet in all_tweets]
        if len(last_tweet_ids) == 0:
          last_tweet_ids = current_tweet_ids
        else:
          # Find new tweet IDs that are not in the last_tweet_ids
          new_tweet_ids = [tweet_id for tweet_id in current_tweet_ids if tweet_id not in last_tweet_ids]

          # Get and print details of new tweets
          for tweet_id in new_tweet_ids:
              tweet_detail = await app.tweet_detail(tweet_id)
              tweet_text = tweet_detail.text
              await tele_bot.send_message(chat_id=CHAT_ID, text=tweet_text)
              try:
                  url = 'http://localhost:' + str(PORT) + '/signal'
                  data = {
                    'message': tweet_text
                  }
                  requests.post(url, json=data)
              except Exception as e:
                  print(e)

          # Update last_tweet_ids to include the current set of tweet IDs
          last_tweet_ids = current_tweet_ids

        # Wait for the specified interval before searching again
        await asyncio.sleep(INTERVAL)

# # Run the main function
asyncio.run(main())
