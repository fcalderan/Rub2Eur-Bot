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

import tweepy # type: ignore
import os
from utils.exchangeRateBot import ExchangeRateBot # type: ignore
from utils.exchangeRateScraper import ExchangeRateScraper # type: ignore
from dotenv import load_dotenv # type: ignore



# ======================================================
# Configuration
# ======================================================

load_dotenv()
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")



# ======================================================
# Classes
# ======================================================

class XClient:
   
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

    def publish(self, text, chart, alt_text, timestamp):
        try:
            media = self.api.media_upload(filename="temp.png", file=chart)
            self.api.create_media_metadata(media.media_id, alt_text)
            self.client.create_tweet(text=text, media_ids=[media.media_id])
            print(f"\n[{timestamp}] Post published successfully on X.")
            print(f"Post Content:\n—————— \n{text}\n——————")
        except tweepy.errors.TooManyRequests:
            print(f"\n[{timestamp}] Too many request.\nVisit https://developer.x.com/en/docs/x-api/rate-limits for further information.\n——————")



# ======================================================
# Initialize components
# ======================================================

scraper = ExchangeRateScraper()
client = XClient(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET, X_BEARER_TOKEN)

# Initialize and start the bot
bot = ExchangeRateBot(scraper, client)
bot.start()
