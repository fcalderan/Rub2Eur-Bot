# Copyright (c) 2024 – today by Fabrizo Calderan. All rights reserved.
# This code is licensed under a non-commercial license.
# You may not use, copy, modify, or distribute this code for commercial purposes.
#
#
# ======================================================
#  Imports
# ======================================================
import warnings
warnings.filterwarnings("ignore", module="urllib3")

import time
import datetime
import pytz     # type: ignore
import tweepy   # type: ignore
import schedule # type: ignore
import os
from utils.exchangeRateScraper import ExchangeRateScraper # type: ignore
from dotenv import load_dotenv # type: ignore



# ======================================================
# Configuration
# ======================================================

PROD_MODE = False

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
OUTPUT_RATE = 1.75 if (PROD_MODE) else 0.0015



# ======================================================
# Classes
# ======================================================

class TwitterBot:
   
    def __init__(self, api_key, api_secret, access_token, access_secret, bearer_token):
        self.auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        self.api = tweepy.API(self.auth)
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )

    def tweet(self, text, chart, alt_text):
        media = self.api.media_upload(filename="temp.png", file=chart)
        self.api.create_media_metadata(media.media_id, alt_text)
        self.client.create_tweet(text=text, media_ids=[media.media_id])
        print("\nTweet posted successfully.")



class ExchangeRateBot:
    
    def __init__(self, scraper, twitter_bot):
        self.scraper = scraper
        self.twitter_bot = twitter_bot


    def tweet_exchange_rate(self):       
        tz = pytz.timezone("Europe/Berlin")
        ts = datetime.datetime.now(tz)
        timestamp = ts.strftime("%d/%m/%y %H:%M")
    
        data  = self.scraper.get_exchange_data()
        rate, trend, chart = data["rate"], data["trend"], data["chart"]

        alt_text = f"#EURRUB exchange rate: {rate:.4f}, as of {timestamp} " 
        alt_text += f"Berlin's time. 5-day trend chart ({trend})."
        
        trend = trend.replace("up by", "↑").replace("down by", "↓")
        tweet = (
            f"🇷🇺🇪🇺 RUB/EUR: {rate:.4f}\n\n"
            f"Data provided by Google Finance, live #RUBEUR rate as " 
            f"of {timestamp} Berlin's time. Trend chart of the last " 
            f"5 days ({trend}). #RussianBankCollapse #RussiaIsCollapsing"
        )

        if PROD_MODE:
            self.twitter_bot.tweet(tweet, chart, alt_text)

        print(f"[{timestamp}] Tweet Content:\n—————— \n{tweet}\n——————\n")

        

    def start(self):
        schedule.every(OUTPUT_RATE).hours.do(self.tweet_exchange_rate).run()
        while True:
            schedule.run_pending()
            time.sleep(1)



# ======================================================
# Initialize components
# ======================================================

scraper = ExchangeRateScraper()
twitter_bot = TwitterBot(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN)

# Initialize and start the bot
bot = ExchangeRateBot(scraper, twitter_bot)
bot.start()