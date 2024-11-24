from tweety import TwitterAsync
import asyncio

async def main():
    app = TwitterAsync("session")  
    # all_tweets = await app.search("CryptoBheem")
    # for t in all_tweets:
    #   print(t)
    d = await app.tweet_detail(1860640399578275998)
    print(d.text)
    # dd = await app.tweet_detail(1781087059249090965)
    # print(dd.text)
    # for tweet in all_tweets:
    #     print(tweet)

asyncio.run(main())
