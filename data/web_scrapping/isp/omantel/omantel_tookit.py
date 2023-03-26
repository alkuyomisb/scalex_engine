import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import ScaleXToolkit


class OmantelToolkit(ScaleXToolkit):
    TOURIST_PACKS_URL = "https://portal.omantel.om/!ut/p/z1/04_iUlDgggP9CCAXKIBMDAhHPyovsSwzPbEkMz8vMUc_Qj8yyizewN3A0cPJwsjH39TN0cDMwMvX1zTI3CnY1ETfSz8Kv4Lg1Dz9guxARQDHGEso/"
    HEYYAK_PLUS_URL = "https://www.omantel.om/Personal/mobile/hayyak/Hayyak-Plus"
    NEW_BAQATI_URL = "https://www.omantel.om/Personal/mobile/New-Baqati"

    def get_omantel_block_value(self, scope_html, title, split=False):
        scope_html_tags = scope_html.select("p.Body-3")
        for tag in scope_html_tags:
            if title in tag.text:  # Although this condition is in a loop, it suppose to be valid on time only
                title_tag = tag.parent.select_one(
                    "p.Body-1.fw-bold")
                if (split):
                    text = self.split_value_and_unit(
                        self.clear_string(title_tag.text))
                else:
                    text = self.clear_string(title_tag.text)

                if "infinity" in str(title_tag):
                    text = "unlimited"
                return text

    # For Hekkay Plus
    def get_omantel_package_title(self, scope_html):
        scope_html_tags = scope_html.select("div._content middle")

    def get_soup(self, URL):
        res = requests.get(URL)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
