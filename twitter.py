from tweety import TwitterAsync
from tweety.filters import SearchFilters
import asyncio
from decouple import config
from telegram import Bot
import aiohttp

AUTH = config("TWITTER_AUTH_TOKEN")
SEARCH_TERM = "from:crypto_zipsy"
INTERVAL = 5 * 60
BOT_TOKEN = config("TWITTER_TELE_BOT_TOKEN")
CHAT_ID = config("CHAT_ID")

PORT = 3000
MAX_TWEETS = 200  # Limit the number of stored IDs

tele_bot = Bot(BOT_TOKEN)

async def main():
    app = TwitterAsync("session")
    await app.load_auth_token(AUTH)
    last_tweet_ids = []

    while True:
        try:
            all_tweets = await app.search(SEARCH_TERM, filter_=SearchFilters.Latest)
            if not all_tweets:
                print("No tweets found. Retrying...")
                await asyncio.sleep(INTERVAL)
                continue
            
            current_tweet_ids = [tweet.id for tweet in all_tweets]
            if len(last_tweet_ids) == 0:
                last_tweet_ids = current_tweet_ids
            else:
                new_tweet_ids = [tweet_id for tweet_id in current_tweet_ids if tweet_id not in last_tweet_ids]
                last_tweet_ids = (last_tweet_ids + new_tweet_ids)[-MAX_TWEETS:]
                for tweet_id in new_tweet_ids:
                    tweet_detail = await app.tweet_detail(tweet_id)
                    tweet_text = tweet_detail.text
                    await tele_bot.send_message(chat_id=CHAT_ID, text=tweet_text)
                    await asyncio.sleep(1)

                    async with aiohttp.ClientSession() as session:
                        try:
                            url = f'http://localhost:{PORT}/signal'
                            data = {'message': tweet_text}
                            await session.post(url, json=data)
                        except Exception as e:
                            print(f"Error posting to server: {e}")
                            
        except Exception as e:
            print(f"Error during Twitter search or processing: {e}")
        
        # Wait for the specified interval before searching again
        await asyncio.sleep(INTERVAL)

# Run the main function
asyncio.run(main())
