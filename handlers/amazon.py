# (c) @AmznUser | Jordan Gill

import os
import re
import requests
from fake_useragent import UserAgent

import config

class Amazon:
    def __init__(self, cookies={}, isLogined=True, amazon_tag=None) -> None:
        self.fullURLRegex = r"https?://(([^\s]*)\.)?amazon\.([a-z.]{2,5})(/d/([^\s]*)|/([^\s]*)/?(?:dp|o|gp|-)/)(aw/d/|product/)?(B[0-9A-Z]{9})([^\s]*)"
        self.shortURLRegex = r"https?://(([^\s]*)\.)?amzn\.to/([0-9A-Za-z]+)"
        self.ua = UserAgent()
        self.user_agent = self.ua.random
        self.amazon_cookies = cookies or config.COOKIES
        self.amazon_tag = amazon_tag or config.AMAZON_TAG
        self.headers = {
            'authority': 'www.amazon.in',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': self.amazon_cookies,
            'device-memory': '8',
            'downlink': '10',
            'dpr': '1.25',
            'ect': '4g',
            'rtt': '50',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '1.25',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-ch-viewport-width': '1007',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent,
            'viewport-width': '1007',
        }

        if config.AMAZON_TLD:
            self.amazon_tld = config.AMAZON_TLD
        else :
            self.amazon_tld = "in"


    def check_cookies(self):
        if not self.amazon_tag:
            status = "Missing AMAZON_TAG env variable"
            return False, status
        return True, self.amazon_tag

    def get_final_url(self, link):
        return requests.get(link, allow_redirects=True).url

    def get_asin_from_full_url(self, url):
        match = re.search(self.fullURLRegex, url)
        return match.group(8) if match is not None else url

    def build_amazon_url(self, asin):
        return f'https://www.amazon.{self.amazon_tld}/dp/{asin}?tag={self.amazon_tag}'

    def generate_url(self, link):
        link = self.get_final_url(link)
        print(link)
        if re.search(self.fullURLRegex, link) :
            newUrl = self.build_amazon_url(self.get_asin_from_full_url(link))
            print(newUrl)
            return {"shortUrl": self.shortenURL(newUrl), "longUrl": newUrl}

    def shortenURL(self, url):
        if self.amazon_cookies:
            params = {
                'longUrl': url,
                'marketplaceId': '44571',
            }

            response = requests.get(
                'https://www.amazon.in/associates/sitestripe/getShortUrl',
                params=params,
                headers=self.headers,
            )
            raw_text = response.text

            try:
                result = response.json()
                if result.get("isOk"):
                    return result.get("shortUrl")
                else:
                    print("Error in Amazon API response: " + str(result))
                    return url
            except Exception as err:
                print("Error in Amazon API response: " + raw_text)
                return url
        else:
            headers = {
                "Authorization": f"Bearer {os.getenv('BIT_LY_TOKEN')}",
                "Content-Type": "application/json"
            }
            body = {
                "long_url": url,
                "domain": "bit.ly"
            }

            try:
                response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=body)
                result = response.json()

                print("Result of Bitly---------->",result)

                if result.get("link"):
                    return result.get("link")
                else:
                    print("Error in Bitly response: " + str(result))
                    return url
            except Exception as err:
                print("Error in Bitly response: " + str(err))
                return url
