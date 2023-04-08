from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from domain.constants.common_data import common_data
from domain.package import Package


class OmantelAfaaq(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.AFFAQ_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white.aqua")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "FIXED",
                "plan_type": "PREPAID",
                "title": "Afaaq",
                "link": self.AFFAQ_URL,
                "isp": "omantel",
            })

            data["download_speed"] = self.get_omantel_block_value(
                block, "Download speed", split=True)
            # data["upload_speed"] = self.get_omantel_block_value(
            #     package_div, "Upload speed", split=True)

            data["data_allowance"] = self.get_omantel_block_value(
                block, "Data", split=True)

            price_tag = block.select_one("div.price")
            data["price"] = self.split_value_and_unit(price_tag.text)
            if "OMR" in price_tag.text:
                data["price"]["unit"] = "OMR"

            if "month" in price_tag.text.lower():
                data["duration"] = {"value": 1, "unit": "MONTH"}

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
