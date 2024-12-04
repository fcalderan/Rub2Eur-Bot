# Copyright (c) 2024 – today by Fabrizo Calderan. All rights reserved.
# This code is licensed under a non-commercial license.
# You may not use, copy, modify, or distribute this code for commercial purposes.
#
#
# ======================================================
#  Imports
# ====================================================== 

import time
import datetime
import pytz     # type: ignore
import schedule # type: ignore



# ======================================================
# Configuration
# ======================================================

PROD_MODE = True
OUTPUT_RATE = 1.25 if (PROD_MODE) else 0.0015



# ======================================================
# Classes
# ======================================================

class ExchangeRateBot:
    
    def __init__(self, scraper, client):
        self.scraper = scraper
        self.client = client


    def publish_exchange_rate(self):       
        tz = pytz.timezone("Europe/Berlin")
        ts = datetime.datetime.now(tz)
        timestamp = ts.strftime("%d/%m/%y %H:%M")
    
        data  = self.scraper.get_exchange_data()
        rate, trend, chart = data["rate"], data["trend"], data["chart"]

        alt_text = f"#EURRUB exchange rate: {rate:.5f}, as of {timestamp} " 
        alt_text += f"Berlin's time. 5-day trend chart ({trend})."
        
        trend = trend.replace("up by", "↑").replace("down by", "↓")
        text = (
            f"🇷🇺🇪🇺 RUB/EUR: {rate:.5f}\n\n"
            f"Data retrieved from @googlefinance, live #RUBEUR rate as " 
            f"of {timestamp} Berlin's time. Trend chart of the last 5 " 
            f"days ({trend}). #RussianBankCollapse #RussiaIsCollapsing"
        )

        if PROD_MODE:
            self.client.publish(text, chart, alt_text, timestamp)
            
        

    def start(self):       
        
        schedule.every(OUTPUT_RATE).hours.do(self.publish_exchange_rate).run()
        while True:
            schedule.run_pending()
            time.sleep(1)