import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import output
from data.web_scrapping.isp.omantel.omantel_tookit import get_omantel_block_value


class Heyyak:
    packages = []
    url = "https://portal.omantel.om/!ut/p/z1/04_iUlDgggP9CCAXKIBMDAhHPyovsSwzPbEkMz8vMUc_Qj8yyizewN3A0cPJwsjH39TN0cDMwMvX1zTI3CnY1ETfSz8Kv4Lg1Dz9guxARQDHGEso/"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")
