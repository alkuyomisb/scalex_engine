from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from domain.package import Package
from domain.constants.common_data import common_data


class OmantelWireless(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.WIRELESS_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white.extra.violet")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "FIXED",
                "plan_type": "POSTPAID",
                "title": "Ultra Fast",
                "link": self.WIRELESS_URL,
                "isp": "omantel",
            })

            data["download_speed"] = self.get_omantel_block_value(
                block, "Download speed", split=True)
            data["upload_speed"] = self.get_omantel_block_value(
                block, "Upload speed", split=True)

            data["data_allowance"] = self.get_omantel_block_value(
                block, "Data")

            if data["data_allowance"] != "UNLIMITED":
                data["data_allowance"] = {
                    "value": float(data["data_allowance"]), "unit": "GB"}

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
