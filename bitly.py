from urllib.parse import urlparse
from dotenv import load_dotenv

import requests
import argparse
import os
import sys


def is_bitlink(url_id, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_id}"
    return requests.get(url, headers=headers).ok


def prepare_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path


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
    bitly_api_token = os.getenv("BITLY_API_TOKEN")
    header = {"Authorization": f"Bearer {bitly_api_token}"}

    parser = argparse.ArgumentParser()
    parser.add_argument('user_url', help='url to be shorted / which to get clicks by')
    args = parser.parse_args()
    user_url = args.user_url

    parsed_url = urlparse(user_url)

    if not parsed_url.scheme:
        print("Url without protocol")
        sys.exit()

    try:
        if is_bitlink(prepare_link(user_url), header):
            print(f"You entered BitLink, count of clicks on it: {get_clicks(prepare_link(user_url), header)}")
        else:
            print(f"Bitlink created: {shorten_link(user_url, header)}")

    except requests.exceptions.HTTPError as err:
        print("An error occurred: \n" + str(err))


if __name__ == "__main__":
    main()