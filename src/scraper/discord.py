import requests
from typing import Any

from util.post import Post
from .base import BaseScraper


class DCScraper(BaseScraper):
    """A class to scrape Discord posts from a given channel."""

    app: Any
    guild_id: str
    channel_id: str
    api_key: str

    def __init__(self, app: Any, guild_id: str, channel_id: str, api_key: str) -> None:
        self.app = app
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.api_key = api_key

    def fetch_latest_post(self) -> Post:
        """Get the latest posts from the Discord channel."""

        headers = {
            "authorization": self.api_key
        }

        params = {
            "limit": 1
        }

        self.app.log("Fetching latest Discord post...", end=" ")

        response = requests.get(f"https://discord.com/api/v9/channels/{self.channel_id}/messages", headers=headers, params=params)
        response.raise_for_status()
        
        self.app.log("Success.", prefix="")

        latest_post = response.json()[0]
        latest_post["guild_id"] = self.guild_id

        return Post.from_discord_post(latest_post)