from typing import Any
from util.post import Post

class BaseScraper:
    """A base class for scraping posts from social media platforms."""

    app: Any
    username: str

    def __init__(self, app: Any, username: str) -> None:
        """Initialize the Scraper class with the given username for the platform.

        Args:
            username (str, optional): The username to scrape.
        """

        self.app = app
        self.username = username

    def fetch_latest_post(self) -> Post:
        """Get the latest post from the account."""

        raise NotImplementedError