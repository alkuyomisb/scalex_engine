import requests
from bs4 import BeautifulSoup
from utils.scalex_toolkit import ScaleXToolkit, get_unit


class AwaserToolkit(ScaleXToolkit):
    FIBER_HOME_URL = "https://awasr.om/en/package/journey/ZVANH"

    def get_download_speed(self, scope_html):
        download_speed_value = scope_html.select_one("span.currency")
        dwonload_speed_unit = scope_html.select_one("span.mo")
        download_speed = {"value": float(
            download_speed_value.text), "unit": get_unit(dwonload_speed_unit.text)}
        return self.unify_unit(download_speed)

    def get_price(self, scope_html):
        price = scope_html.select_one("p.price")
        return self.split_value_and_unit(self.clear_string(price.text))

    def get_other(self, scope_html):
        other = []
        promotions = scope_html.select_one(
            "div.service-plan-content.text-direction")
        li = promotions.find_all("li")
        for l in li:
            if "Get Increased" not in l.text:
                other.append(self.clear_string(l.text))
        return other

    def get_soup(self, URL):
        res = requests.get(URL)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
