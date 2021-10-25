from urllib.parse import urlparse
from dotenv import load_dotenv

import requests
import os


def is_bitlink(url):
    if urlparse(url)[1] == "bit.ly":
        return True
    return False


class Bitly:

    def __init__(self, api_token):
        self.apiToken = api_token
        self.header = {'Authorization': 'Bearer {}'.format(self.apiToken)}

    def shorten_link(self, longurl):

        payload = {"long_url": longurl}
        url = "https://api-ssl.bitly.com/v4/shorten"
        response = requests.post(url, headers=self.header, json=payload)
        if response.ok:
            shorten = response.json()['link']
            return shorten
        else:
            raise requests.exceptions.HTTPError

    def get_clicks(self, shorturl):

        url = f"https://api-ssl.bitly.com/v4/bitlinks/{shorturl}/clicks/summary"
        response = requests.get(url, headers=self.header)
        if response.ok:
            return response.json()["total_clicks"]
        else:
            raise requests.exceptions.HTTPError


def main():
    load_dotenv()
    api_token = os.getenv("api_token")
    bitly = Bitly(api_token)

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
