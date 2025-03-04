import re
import requests

from .base import BaseScraper
from post import Post
from utils import USER_AGENT

class IGScraper(BaseScraper):
    """A class to scrape instagram posts from a given account."""
    
    username: str

    def _get_app_id(self) -> str:
        """Get the Instagram app ID.
        This is necessary to make requests to the Instagram API.
        """
        
        response = requests.get(f'https://www.instagram.com/{self.username}')
        response.raise_for_status()
        
        return re.search(r'appId":"(\d*)', response.text)[1]

    def fetch_latest_post(self) -> Post:
        """Get the latest posts from the Instagram account."""

        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.username}"

        headers = {
            "x-ig-app-id": self._get_app_id(),
            "User-Agent": USER_AGENT,
        }

        print("Fetching latest Instagram post...", end=" ")
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        print("Success.")
        
        latest_post = response.json()["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]
        return Post.from_instagram_post(latest_post)