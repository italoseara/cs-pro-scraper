import json
import requests
from bs4 import BeautifulSoup

from .base import BaseScraper
from post import Post
from utils import USER_AGENT, find_in_object

class FBScraper(BaseScraper):
    """A class to scrape facebook posts from a given account."""
    
    username: str

    def fetch_latest_post(self) -> Post:
        """Get the latest posts from the Facebook account."""

        url = f"https://www.facebook.com/{self.username}"
        
        headers = {
            "accept": "text/html",
            "User-Agent": USER_AGENT
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the script tag containing the post data
        info = None
        for script in soup.find_all("script"):
            if "adp_ProfileCometTimelineFeedQueryRelayPreloader" in script.text and\
                "comet_photo_attachment_resolution_renderer" in script.text:
                info = json.loads(script.text)
                break

        # Extract the latest post data
        result = find_in_object(info, ["result", "data", "user"])
        latest_post = result["timeline_list_feed_units"]["edges"][0]["node"]["comet_sections"]

        return Post.from_facebook_post(latest_post)