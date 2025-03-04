from post import Post

class BaseScraper:
    """A base class for scraping posts from social media platforms."""

    username: str

    def __init__(self, username: str) -> None:
        """Initialize the Scraper class with the given username for the platform.

        Args:
            username (str, optional): The username to scrape.
        """

        self.username = username

    def fetch_latest_post(self) -> Post:
        """Get the latest post from the account."""

        raise NotImplementedError