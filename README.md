# Promocode Scraper

![GitHub License](https://img.shields.io/github/license/italoseara/cs-pro-scraper)
![GitHub Last commit](https://img.shields.io/github/last-commit/italoseara/cs-pro-scraper/main)

This project is a scraper for the gambling website [cs.pro](https://cs.pro). The scraper collects promotional codes from the website's social media accounts.

> [!CAUTION]
> Use this scraper at your own risk. Scraping social media platforms can be against their terms of service. Ensure you understand and comply with the terms of service of each platform before using this scraper.

> [!IMPORTANT]
> Gambling can be addictive and harmful. Please gamble responsibly. If you or someone you know has a gambling problem, seek help from professional organizations.

## Features

- Scrapes promocodes from various social media platforms.
- Supports Instagram, Facebook, X (formerly Twitter), and Discord.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/italoseara/cs-pro-scraper.git
   cd cs-pro-scraper
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:

   - Windows:

     Check the [Official Tesseract OCR Installation Guide](https://github.com/UB-Mannheim/tesseract/wiki) for Windows.

   - Linux:

     ```sh
     sudo apt install tesseract-ocr
     ```

   - macOS:

     ```sh
     brew install tesseract
     ```

4. Create a file in the root directory called `.env` and add the following environment variables:

   ```env
   IG_USERNAME=your_instagram_username
   FB_USERNAME=your_facebook_username
   X_USERNAME=your_x_username
   
   DISCORD_GUILD_ID=your_discord_guild_id
   DISCORD_CHANNEL_ID=your_discord_channel_id
   ```

> [!NOTE]
> The `DISCORD_GUILD_ID` and `DISCORD_CHANNEL_ID` can be obtained by activating the Developer Mode in Discord and right-clicking on the guild and channel, respectively to copy their IDs.

## Usage

Run the scraper:

```sh
python src/main.py
```

Fill the input fields with the required information and press the "Force Start" button.

> [!NOTE]
> The `X Auth Token` and `X CSRF Token` are required for the X scraper. They can be obtained by inspecting the X website and looking for the `auth_token` and `ct0` keys respectively in the Application tab in the Cookies section.
>
> The `Discord API Key` can be obtained by looking for the `Authorization` header in the Network tab of the Discord website.
>
> The `CS.PRO Cookie` can be obtained by logging into the [cs.pro](https://cs.pro) website with steam and copying the `sfRemember` cookie. If you dont provide this, the scraper will not try to activate the promocodes by itself.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
