import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import ScaleXToolkit


class FriendlyToolkit(ScaleXToolkit):
    FRIENDLY_MOBILE_URL = "https://www.friendimobile.com/en-om/section/freedom-plans-en"

    def get_soup(self, URL):
        res = requests.get(URL)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
