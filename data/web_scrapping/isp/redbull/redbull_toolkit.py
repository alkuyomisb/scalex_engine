import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import ScaleXToolkit


class RedbullToolkit(ScaleXToolkit):
    MOBILE_PLANS_URL = "https://www.redbullmobile.om/en/plans/"

    def get_soup(self, URL):
        res = requests.get(URL)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
