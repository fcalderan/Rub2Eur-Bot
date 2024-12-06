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
import requests # type: ignore


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



    def is_connection_available(self, timestamp):
        try:
            # Verifica la connessione facendo una richiesta a google.com
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            print(f"\n[{self.timestamp}] Connection error: no internet connection.")
            return False
        except requests.Timeout:
            print(f"\n[{self.timestamp}] Timeout error: the request timed out.")
            return False
        except requests.RequestException as e:
            print(f"\n[{self.timestamp}] Request failed: {e}")
            return False
            
    

    def try_publish(self):
        tz = pytz.timezone("Europe/Berlin")
        ts = datetime.datetime.now(tz)
        self.timestamp = ts.strftime("%d/%m/%y %H:%M")

        if self.is_connection_available():            
            self.do_publish()
        else:
            print(f"\n[{self.timestamp}] Post not published.\n")



    def do_publish(self, timestamp):           
        data  = self.scraper.get_exchange_data()
        rate, trend, chart = data["rate"], data["trend"], data["chart"]

        alt_text = f"#EURRUB exchange rate: {rate:.5f}, as of {self.timestamp} " 
        alt_text += f"Berlin's time. 5-day trend chart ({trend})."
        
        trend = trend.replace("up by", "↑").replace("down by", "↓")
        text = (
            f"🇷🇺🇪🇺 RUB/EUR: {rate:.5f}\n\n"
            f"Data retrieved from @googlefinance, live #RUBEUR rate as " 
            f"of {self.timestamp} Berlin's time. Trend chart of the last 5 " 
            f"days ({trend}). #RussianBankCollapse #RussiaIsCollapsing"
        )

        self.client.publish(text, chart, alt_text, self.timestamp, PROD_MODE)
        
        

    def start(self):       
        
        schedule.every(OUTPUT_RATE).hours.do(self.try_publish).run()
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nProcess interrupted by user (Ctrl+C). Exiting gracefully.\n\n")
            exit(0)
