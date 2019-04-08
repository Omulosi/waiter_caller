import urllib
import json
from config import Config

TOKEN = Config.OAUTH_TOKEN
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = urllib.request.urlopen(url).read()
            jr = json.loads(response.decode('utf-8'))
            return jr['data']['url']
        except Exception as e:
            print(e) 