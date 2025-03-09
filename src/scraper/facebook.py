import json
import requests
from bs4 import BeautifulSoup
from typing import Any

from util.post import Post
from util.misc import USER_AGENT, find_in_object
from .base import BaseScraper

class FBScraper(BaseScraper):
    """A class to scrape facebook posts from a given account."""

    app: Any
    username: str

    def fetch_latest_post(self) -> Post:
        """Get the latest posts from the Facebook account."""

        url = f"https://www.facebook.com/{self.username}"
        
        headers = {
            "accept": "text/html",
            "User-Agent": USER_AGENT
        }

        self.app.log("Fetching latest Facebook post...", end=" ")

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

        self.app.log("Success.", prefix="")

        return Post.from_facebook_post(latest_post)