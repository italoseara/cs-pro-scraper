import bs4
import json
import logging
from typing import Any
from seleniumbase import Driver


def get(url: str, cookies: list[dict[str, str]] = None, params: dict[str, str] = None) -> Any:
    """Make a GET request to a URL bypassing Cloudflare protection (it may be a lot slower than a normal request).

    Args:
        url (str): The URL to make the request to
        cookies (list[dict[str, str]]): A list of cookies to inject
        params (dict[str, str]): A dictionary of parameters to send with the request

    Returns:
        Any: The response from the request
    """
    
    base_url = url.split("/")[2] if url.startswith("http") else url.split("/")[0]
    full_url = url if url.startswith("http") else f"https://{url}"

    if params:
        full_url += "?" + "&".join([f"{key}={value}" for key, value in params.items()]) # Add the params to the URL

    # Disable the logs
    logging.getLogger("seleniumbase").setLevel(logging.CRITICAL)

    # Create the driver with headless option
    driver = Driver(uc=True, headless=True)
    
    # Inject the cookies
    if cookies:
        driver.uc_open_with_reconnect(base_url, 1)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # Open the URL
    driver.uc_open_with_reconnect(full_url, 2)
    driver.uc_gui_click_captcha()

    # Return the page source
    soup = bs4.BeautifulSoup(driver.get_page_source(), "html.parser")
    driver.quit()

    try:
        return json.loads(soup.text)
    except json.JSONDecodeError:
        return None  # Shouldn't happen unless the bypass fails


if __name__ == "__main__":
    url = "https://csgocases.com/api.php/add_wallet_code"
    params = { "code": "123456" }
    cookies = [{ "name": "sfRemember", "value": "cw2tntc9xggg4s48844sggo4sogoso0" }]

    response = get(url, cookies, params)
    print(response)