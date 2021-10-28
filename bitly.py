from urllib.parse import urlparse
from dotenv import load_dotenv

import requests
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


def is_bitlink(id, headers):
    url_ = f"https://api-ssl.bitly.com/v4/bitlinks/{id}"
    return requests.get(url_, headers=headers).ok


class Bitly:

    def __init__(self, api_token):
        self.apiToken = api_token
        self.header = {'Authorization': 'Bearer {}'.format(self.apiToken)}

    def shorten_link(self, longurl):

        payload = {"long_url": longurl}
        url = "https://api-ssl.bitly.com/v4/shorten"
        response = requests.post(url, headers=self.header, json=payload)
        response.raise_for_status()
        return response.json()["link"]

    def get_clicks(self, shorturl):

        url = f"https://api-ssl.bitly.com/v4/bitlinks/{shorturl}/clicks/summary"
        response = requests.get(url, headers=self.header)
        response.raise_for_status()
        return response.json()["total_clicks"]


def main():

    bitly = Bitly(API_TOKEN)

    user_url = input("Enter your URL\n")

    try:
        if is_bitlink(user_url):
            url_id = urlparse(user_url)[1] + urlparse(user_url)[2]
            count = bitly.get_clicks(url_id)
            print(f"You entered BitLink, count of clicks on it : {count}")

        else:
            short_link = bitly.shorten_link(user_url)
            print(f"url created \n" + short_link)

    except requests.exceptions.HTTPError:
        print("Invalid url :-(")


if __name__ == '__main__':
    main()
