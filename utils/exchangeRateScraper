# Copyright (c) 2024 – today by Fabrizo Calderan. All rights reserved.
# This code is licensed under a non-commercial license.
# You may not use, copy, modify, or distribute this code for commercial purposes.
#
#
# ======================================================
#  Imports
# ======================================================

from io import BytesIO
from playwright.sync_api import sync_playwright # type: ignore

URL = "https://www.google.com/finance/quote/RUB-EUR?window=5D"


class ExchangeRateScraper:

    def get_exchange_data(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                extra_http_headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "sec-ch-ua": "Not A(Brand';v='99', 'Google Chrome';v='121', 'Chromium';v='121'",
                    "referer": "https://www.google.com/"
                }
            )
            page = context.new_page()
            page.goto(URL)

            try:
                page.wait_for_selector("span:has-text('Accept all')", timeout=5000)
                page.click("span:has-text('Accept all')")
            except Exception:
                print("No consent dialog found.")

            page.wait_for_load_state("networkidle")
            page.wait_for_selector('[data-last-price]', timeout=5000)

            rate = float(page.query_selector('[data-last-price]').get_attribute('data-last-price'))
            trend = page.query_selector('[data-last-price] span[aria-label]').get_attribute('aria-label').lower()
            chart = page.query_selector('div[aria-hidden][jslog]')
            chart = chart.screenshot(path=None)
            
            # Creates an in-memory binary object
            chart = BytesIO(chart)
            browser.close()

            return {"rate": rate, "trend": trend, "chart": chart}


