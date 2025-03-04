import os
from dotenv import load_dotenv

from post import Post
from scraper import *

load_dotenv()


def main() -> None:
    # Initialize the scrapers
    scrapers: list[BaseScraper] = [
        # Instagram is very strict with scraping
        # se we need to remember to not abuse it
        # IGScraper(username=os.getenv("IG_USERNAME")),

        FBScraper(username=os.getenv("FB_USERNAME")),
        
        XScraper(username=os.getenv("X_USERNAME"),
                 auth_token=os.getenv("X_AUTH_TOKEN"),
                 csrf_token=os.getenv("X_CSRF_TOKEN")),
        
        DCScraper(guild_id=os.getenv("DISCORD_GUILD_ID"),
                  channel_id=os.getenv("DISCORD_CHANNEL_ID"),
                  api_key=os.getenv("DISCORD_API_KEY"))
    ]

    # Fetch the latest posts from each social media platform
    posts: list[Post] = []
    for scraper in scrapers:
        posts.append(scraper.fetch_latest_post())
    
    # Show the images using the PIL library
    for post in posts:
        post.image.show()
    

if __name__ == '__main__':
    main()