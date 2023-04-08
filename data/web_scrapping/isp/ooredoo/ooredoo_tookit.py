import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import ScaleXToolkit


class OoredooToolkit(ScaleXToolkit):
    # URLs Section
    SHAHRY_DATA_ONLY_URL = "https://www.ooredoo.om/Personal/Mobile/Shahry(Postpaid)/ShahryDataOnlyPlans.aspx"
    OMANUNA_URL = "https://www.ooredoo.om/Personal/Mobile/Shahry(Postpaid)/OmanunaPlans.aspx"
    SHAHRY_ENDLESS_URL = "https://www.ooredoo.om/Personal/Mobile/Shahry(Postpaid)/ShahryEndless.aspx"
    HALA_SIM_URL = "https://www.ooredoo.om/Personal/Mobile/Hala(Prepaid)/HalaSIM.aspx"
    HALA_PLANS_URL = "https://www.ooredoo.om/Personal/Mobile/Hala(Prepaid)/HalaPlans.aspx"
    TOURIST_PLANS_URL = "https://www.ooredoo.om/Personal/Mobile/Promotions/FIFATouristPack.aspx"
    SATELLITE_HOME_INTERNET_URL = "https://www.ooredoo.om/Personal/Home/SatelliteHomeInternet.aspx"
    FIVE_G_HOME_INTERNET_URL = "https://www.ooredoo.om/Personal/Home/5GHomeInternet.aspx"
    FIBER_HOME_INTERNET_URL = "https://www.ooredoo.om/Personal/Home/FibreHomeInternet.aspx"
    FOUR_G_HOME_INTERNET_URL = "https://www.ooredoo.om/Personal/Home/4GHomeInternet.aspx"

    # Functions Section
    def get_ooredoo_block_value(self, scope_html, title, split=False, match_str=False, title_tag="span", value_tag="p", title_class_str="", value_class_str=""):
        span_tags = scope_html.select(title_tag+title_class_str)
        res = {"value": 0, "unit": ""} if split else ""
        for span in span_tags:
            if (title.lower() in span.text.lower() and not match_str) or (title.lower().strip() == span.text.lower().strip() and match_str):
                try:
                    parent = span.parent
                    target = parent.select_one(value_tag+value_class_str).text
                    if (split):
                        text = self.split_value_and_unit(
                            self.clear_string(target))
                    else:
                        text = self.clear_string(target)
                    if "infinity" in str(target):
                        text = "unlimited"
                    return text if text is not None else res
                except:
                    return res
        return res

    def get_soup(self, URL):
        res = requests.get(URL, verify=False)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
