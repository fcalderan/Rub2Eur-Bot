# RUB2EUR Bot

A Python-based bot that scrapes exchange rate data from Google Finance and periodically posts the RUB/EUR exchange rate to specified platforms, such as X/Twitter or BlueSky.

## Project Overview

This project automates the retrieval and publication of exchange rate data for the Russian Ruble (RUB) and Euro (EUR). It uses:

- **Playwright**: For web scraping exchange rate data and generating visual snapshots.
- **Tweepy**: For interacting with X/Twitter's API to post updates.
- **BlueSky Client**: For posting updates to the decentralized BlueSky platform.
- **Modular Code Structure**: Organized into reusable components for scraping and platform-specific interactions.

### Key Features

- Fetches real-time exchange rates and trends.
- Takes screenshots of exchange rate charts without saving to disk (uses in-memory processing).
- Posts updates to XTwitter and BlueSky, ensuring accessibility with alt-text descriptions.
- Configurable schedule for periodic updates.

## Project Structure

- `utils/`: Contains reusable components for scraping and posting.
  - `exchangeRateScraper.py`: Handles web scraping logic.
  - `exchangeRateBot.py`: Encapsulates platform-specific logic.
- `.env`: Stores sensitive API credentials securely.
- `rub2eur-X.py`: The main entry point for the X/Twitter bot.
- `rub2eur-bsky.py`: The main entry point for the BlueSky bot.

### Why This Organization?

The modular design makes it easy to:

- Reuse or change scraping logic (exchangeRateScraper.py) .
- Reuse or change post composition and automation (exchangeRateBot.py).
- Securely manage credentials through the .env file.


## How to Set Up and Run Locally

### Prerequisites

1. Install Python 3.8 or higher.
2. Install the required libraries:
   ```bash
   pip install playwright tweepy python-dotenv
   playwright install


### Configuration
Create a `.env` file in the root directory with the following variables:

    # X/Twitter API credentials
    X_API_KEY=your_api_key
    X_API_SECRET=your_api_secret
    X_ACCESS_TOKEN=your_access_token
    X_ACCESS_SECRET=your_access_secret
    X_BEARER_TOKEN=your_bearer_token
    
    # BlueSky API credentials
    BSKY_USERNAME=your_bsky_username
    BSKY_PASSWORD=your_bsky_password
    
Replace placeholder values with your actual credentials.

For X/Twitter, learn how to obtain these credentials from the [X/Twitter Developer Portal](https://developer.x.com/en).

### Running the Bot

For X/Twitter:

    python rub2eur-X.py

For BlueSky:

    python rub2eur-bsky.py

The bot will immediately fetch exchange rates, post updates, and schedule further executions.


**Example Output**
A sample Xeet/Tweet or BlueSky post:

> 🇷🇺🇪🇺 RUB/EUR: 0.00896  
Live #RUBEUR rate as of 01/01/2024 12:00 Berlin's time. Chart of the trend for the last 5 days.
#RussianBankCollapse #RussiaIsCollapsing

<img src="https://res.cloudinary.com/fabdev-/image/upload/v1733499225/rub2eur-X-bot_xqpdrl.png" alt="Preview" width="360" />

## License

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> - You can't use this software or parts of them for **commercial purpose**;
> - You must always give credit to the author and keep the comments in the files.
>
> THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
