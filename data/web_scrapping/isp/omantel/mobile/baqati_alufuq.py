from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelBaqatiAlufuq(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.ALUFUQ_PLAN)
        self.get_packages()

    def get_packages(self):
        data = common_data.copy()
        data.update({
            "service_type": "MOBILE",
            "plan_type": "POSTPAID",
            "title": "Al Ufuq",
            "link": self.ALUFUQ_PLAN,
            "isp": "omantel",
        })

        # Price
        price_tag = self.soup.select_one(
            "div.price")
        data["price"] = self.split_value_and_unit(price_tag.text)
        if "OMR" in price_tag.text:
            data["price"]["unit"] = "OMR"

        # Duration
        if "MONTH" in price_tag.text:
            data["duration"] = {"value": 1, "unit": "MONTH"}

        # Internationl Minutes
        td_tags = self.soup.select(
            "td")

        for td in td_tags:
            try:
                title = td.select_one(
                    "h6.text-start").text
                value = td.select_one("h4.text-end").text
                if "Data" in title:
                    data["data_allowance"] = value.upper()
                elif "National minutes" in title:
                    data["local_minutes"] = value.upper()
                elif "International min" in title:
                    data["international_minutes"] = self.find_number(value, [
                                                                     "min"])
                elif "SMS" in title:
                    data["sms"] = value.upper()
            except:
                pass
        package = Package(data)
        self.packages.append(package)

    def reset(self):
        self.packages = []
