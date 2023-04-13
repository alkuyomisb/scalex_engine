import requests
from bs4 import BeautifulSoup
from utils.scalex_toolkit import ScaleXToolkit


class OmantelToolkit(ScaleXToolkit):
    TOURIST_PACKS_URL = "https://portal.omantel.om/!ut/p/z1/04_iUlDgggP9CCAXKIBMDAhHPyovsSwzPbEkMz8vMUc_Qj8yyizewN3A0cPJwsjH39TN0cDMwMvX1zTI3CnY1ETfSz8Kv4Lg1Dz9guxARQDHGEso/"
    HEYYAK_PLUS_URL = "https://www.omantel.om/Personal/mobile/hayyak/Hayyak-Plus"
    NEW_BAQATI_URL = "https://www.omantel.om/Personal/mobile/New-Baqati"
    DATA_ONLY_URL = "https://www.omantel.om/Personal/mobile/Hayyak-Data-only-Plan"
    AMAN_PAN = "https://www.omantel.om/!ut/p/z0/04_Sj9CPykssy0xPLMnMz0vMAfIjo8ziDdwNHD2cLIx8_E3dHA3MDLx8fU2DzIN8ncz0C7IdFQFRPZ7B/"
    ALUFUQ_PLAN = "https://www.omantel.om/Personal/mobile/New-Baqati/baqati-al-ufuq"
    ERADA_BAQATI = "https://www.omantel.om/Personal/mobile/New-Baqati/New-Baqati-Addon/Erada-Baqati"
    AMAN_POSTPAID = "https://www.omantel.om/!ut/p/z0/04_Sj9CPykssy0xPLMnMz0vMAfIjo8ziDdwNHD2cLIx8_E3dHA3MDLx8fU2DzIM8XM31C7IdFQEe3oWH/"
    JAWAZK_GCC_URL = "https://www.omantel.om/Personal/mobile/Roaming/jawazak-gcc"
    JAWAZK_WORLD_URL = "https://www.omantel.om/Personal/mobile/Roaming/Jawazak-World"
    ULTRA_FAST_URL = "https://www.omantel.om/Personal/AtHome/basic/ultra-fast"
    BASIC_URL = "https://www.omantel.om/Personal/AtHome/basic"
    WIRELESS_URL = "https://www.omantel.om/Personal/AtHome/5G-Home-offer"
    AFFAQ_URL = "https://www.omantel.om/Personal/AtHome/Afaaq"
    FIXED_LINE_URL = "https://www.omantel.om/Personal/AtHome/Fixed-Line"

    def get_omantel_block_value(self, scope_html, title, split=False):
        scope_html_tags = scope_html.select("p.Body-3")
        for tag in scope_html_tags:
            # Although this condition is in a loop, it suppose to be valid on time only
            if title.lower() in tag.text.lower():

                title_tag = tag.parent.select_one(
                    "p.Body-1.fw-bold")

                if "infinity" in str(title_tag):
                    text = "UNLIMITED"
                else:
                    if (split):
                        text = self.split_value_and_unit(
                            self.clear_string(title_tag.text))
                    else:
                        text = self.clear_string(title_tag.text)
                return text

    def get_omantel_package_title(self, scope_html):
        scope_html_tags = scope_html.select("div._content middle")

    def get_soup(self, URL):
        res = requests.get(URL)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
