from urllib.parse import urlparse
from dotenv import load_dotenv

import requests
import os


def is_bitlink(url_id, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_id}"
    return requests.get(url, headers=headers).ok


def shorten_link(long_url, header):
    payload = {"long_url": long_url}
    url = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url, headers=header, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def get_clicks(short_url, header):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{short_url}/clicks/summary"
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response.json()["total_clicks"]


def main():
    load_dotenv()
    BITLY_API_TOKEN = os.getenv("BITLY_API_TOKEN")

    header = {"Authorization": f"Bearer {BITLY_API_TOKEN}"}
    user_url = input("Enter your URL\n")

    try:
        parsed_url = urlparse(user_url)
        url_id = f"{parsed_url[1]}{parsed_url[2]}"

        if is_bitlink(url_id, header):
            print(f"You entered BitLink, count of clicks on it: {get_clicks(url_id, header)}")
        else:
            print(f"Bitlink created: {shorten_link(user_url, header)}")

    except requests.exceptions.HTTPError:
        print("Wrong url")


if __name__ == "__main__":
    main()