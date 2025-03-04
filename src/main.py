import os
import json
import schedule
from time import sleep
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

from promocode import PromocodeReader
from post import Post
from scraper import *

load_dotenv()


class App:
    def __init__(self) -> None:
        self.scrapers = [
            # Instagram is very strict with scraping se we need to remember to not abuse it
            # IGScraper(username=os.getenv("IG_USERNAME")),

            FBScraper(username=os.getenv("FB_USERNAME")),
            
            XScraper(username=os.getenv("X_USERNAME"),
                    auth_token=os.getenv("X_AUTH_TOKEN"),
                    csrf_token=os.getenv("X_CSRF_TOKEN")),
            
            DCScraper(guild_id=os.getenv("DISCORD_GUILD_ID"),
                    channel_id=os.getenv("DISCORD_CHANNEL_ID"),
                    api_key=os.getenv("DISCORD_API_KEY"))
        ]

    def run(self) -> None:
        latest_posts = [scraper.fetch_latest_post() for scraper in self.scrapers]
        promocode_posts = [post for post in latest_posts if "promocode" in post.text.lower()]

        expired_promocodes = self.load_expired_promocodes()
        new_promocodes = self.extract_valid_promocodes(promocode_posts, expired_promocodes)

        self.update_expired_promocodes(expired_promocodes, new_promocodes)

        for promocode, post in new_promocodes:
            print(f"New promocode found: {promocode}")
            self.broadcast(promocode, post)

    @staticmethod
    def broadcast(promocode: str, post: Post) -> None:
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not webhook_url:
            print("No webhook URL provided. Skipping broadcast.")
            return
        
        webhook = DiscordWebhook(url=webhook_url, content='@everyone')

        embed = DiscordEmbed(title=f"New promocode `{promocode}`", description=f"Click [here]({post.url}) to see the post", color="6dc176")
        embed.set_author(name="csgocases.com", 
                        icon_url="https://csgocases.com/images/avatar.jpg", 
                        url=post.author_url)
        embed.set_image(url=post.image_url)
        embed.set_timestamp()

        webhook.add_embed(embed)
        
        response = webhook.execute()
        if response.ok:
            print('Webhook message sent')
        else:
            print('Could not send the webhook message')

    @staticmethod
    def load_expired_promocodes() -> list[str]:
        if os.path.exists("promocodes.json"):
            with open("promocodes.json", "r") as file:
                return json.load(file)
        return []

    @staticmethod
    def extract_valid_promocodes(posts: list[Post], expired_promocodes: list[str]) -> list[tuple[str, Post]]:
        return [
            (code, post) for post in posts
            if (code := PromocodeReader(post.image).extract()) not in expired_promocodes
        ]

    @staticmethod
    def update_expired_promocodes(expired_promocodes: list[str], new_promocodes: list[tuple]) -> None:
        expired_promocodes.extend(code for code, _ in new_promocodes)
        with open("promocodes.json", "w") as file:
            json.dump(expired_promocodes, file)


def main() -> None:
    app = App()
    app.run()


if __name__ == '__main__':
    main()