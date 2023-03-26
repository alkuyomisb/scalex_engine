import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import ScaleXToolkit


class AwaserToolkit(ScaleXToolkit):
    FIBER_HOME_URL = "https://awasr.om/en/package/journey/ZVANH"

    def get_download_speed(self, scope_html):
        download_speed_value = scope_html.select_one("span.currency")
        dwonload_speed_unit = scope_html.select_one("span.mo")
        return {"value": download_speed_value.text, "unit": dwonload_speed_unit.text}

    def get_title(self, scope_html):
        try:
            title_img_tag = scope_html.select_one(
                "img.service-plan-title-image")
            return {"value": "https://awasr.om"+title_img_tag["src"], "format": "IMG_URL"}
        except:
            print("Couldn't get title image")

    def get_price(self, scope_html):
        price = scope_html.select_one("p.price")
        return self.split_value_and_unit(self.clear_string(price.text))

    def get_other(self, scope_html):
        other = []
        promotions = scope_html.select_one(
            "div.service-plan-content.text-direction")
        li = promotions.find_all("li")
        for l in li:
            other.append(self.clear_string(l.text))
        return other

    def get_soup(self, URL):
        res = requests.get(URL)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
