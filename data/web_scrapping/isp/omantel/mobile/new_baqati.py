from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelNewBaqati(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.NEW_BAQATI_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "POSTPAID",
                "title": "New Baqati",
                "link": self.NEW_BAQATI_URL,
                "isp": "omantel",
            })

            self.get_omantel_package_title(block)

            data["local_minutes"] = self.get_omantel_block_value(
                block, "Local Minutes")

            data["local_minutes"] = self.find_number(
                data["local_minutes"], ["min"])

            data["international_minutes"] = self.get_omantel_block_value(
                block, "Int’l Minutes")

            data["international_minutes"] = self.find_number(
                data["international_minutes"], ["min"])

            data["data_allowance"] = self.get_omantel_block_value(
                block, "GCC Data", split=True)

            if data["data_allowance"] == None:
                data["data_allowance"] = "UNLIMITED"

            data["world_roaming_data"] = self.split_value_and_unit(self.get_omantel_block_value(
                block, "World Roaming Data"))

            price_tag = block.select_one("div.price")

            data["price"] = self.split_value_and_unit(price_tag.text)

            if "OMR" in price_tag.text:
                data["price"]["unit"] = "OMR"

            if "month" in price_tag.text:
                data["duration"] = {"value": 1, "unit": "MONTH"}

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
