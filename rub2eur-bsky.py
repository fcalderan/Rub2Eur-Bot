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

from atproto import Client # type: ignore
import os
from utils.exchangeRateBot import ExchangeRateBot # type: ignore
from utils.exchangeRateScraper import ExchangeRateScraper # type: ignore
from dotenv import load_dotenv # type: ignore



# ======================================================
# Configuration
# ======================================================

load_dotenv()
BSKY_USERNAME = os.getenv("BSKY_USERNAME")
BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")



# ======================================================
# Classes
# ======================================================

class BlueskyClient:
   
    def __init__(self, username, password):       
        self.client = Client()
        self.client.login(username, password)

    def publish(self, text, chart, alt_text, timestamp, prod_mode):
        if prod_mode:
            try:
                #response = self.client.send_image(text=text, image=chart, image_alt=alt_text)
                response = self.client.send_post(text=text)   
                print(f"\n[{timestamp}] Post successfully published on Bluesky.")
                print(f"Response:\n  [uri] {response.uri}\n  [cid] {response.cid}\n——————")
                
            except:
                print(f"\n[{timestamp}] Error posting on Bluesky. Visit https://docs.bsky.app/docs/advanced-guides/rate-limits for furher information.\n——————")
                
        print(f"Post Content:\n—————— \n{text}\n——————")


# ======================================================
# Initialize components
# ======================================================

client = BlueskyClient(BSKY_USERNAME, BSKY_PASSWORD)
scraper = ExchangeRateScraper()

# Initialize and start the bot
bot = ExchangeRateBot(scraper, client)
bot.start()
