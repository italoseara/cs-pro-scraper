from PIL.Image import Image

from utils import download_image


class Post:
    """A class to represent a social media post."""

    author: str
    author_url: str
    text: str
    image: Image
    url: str

    def __init__(self, author: str, author_url: str, text: str, image: Image, url: str) -> None:
        self.author = author
        self.author_url = author_url
        self.text = text
        self.url = url

        # Download and resize the image to 512x512
        self.image = download_image(image)
        self.image.thumbnail((512, 512))

    @staticmethod
    def from_instagram_post(post: dict) -> "Post":
        """Create a Post object from an Instagram post."""

        return Post(
            author=post["owner"]["username"],
            author_url=f"https://www.instagram.com/{post['owner']['username']}",
            text=post["edge_media_to_caption"]["edges"][0]["node"]["text"],
            image=post["display_url"],
            url=f"https://www.instagram.com/p/{post['shortcode']}",
        )

    @staticmethod
    def from_facebook_post(post: dict) -> "Post":
        """Create a Post object from a Facebook post."""

        return Post(
            author=post["content"]["story"]["actors"][0]["name"],
            author_url=post["content"]["story"]["actors"][0]["url"],
            text=post["content"]["story"]["message"]["text"],
            image=post["content"]["story"]["attachments"][0]["styles"]["attachment"]["media"]\
                ["comet_photo_attachment_resolution_renderer"]["image"]["uri"],
            url=post["content"]["story"]["wwwURL"],
        )

    @staticmethod
    def from_x_post(post: dict) -> "Post":
        """Create a Post object from a X post."""

        return Post(
            author=post["user"]["screen_name"],
            author_url=post["user"]["url"],
            text=post["full_text"],
            image=post["entities"]["media"][0]["media_url_https"],
            url=post["entities"]["media"][0]["url"],
        )

    def from_discord_post(post: dict) -> "Post":
        """Create a Post object from a Discord post."""

        return Post(
            author=post["author"]["global_name"],
            author_url=f"https://discord.com/users/{post['author']['id']}",
            text=post["content"],
            image=post["attachments"][0]["url"],
            url=f"https://discord.com/channels/{post['guild_id']}/{post['channel_id']}/{post['id']}",
        )