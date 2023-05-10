from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelEradaBaqati(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.ERADA_BAQATI)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "POSTPAID",
                "title": "Erada Baqati",
                "link": self.ERADA_BAQATI,
                "isp": "omantel",
            })

            self.get_omantel_package_title(block)
            data["local_minutes"] = self.get_omantel_block_value(
                block, "Local Minutes")

            if type(data["local_minutes"]) == dict:
                data["local_minutes"] = data["local_minutes"]["value"]
            elif data["local_minutes"] != "UNLIMITED":

                data["local_minutes"] = self.find_number(
                    data["local_minutes"], ["min"])

            data["international_minutes"] = self.split_value_and_unit(self.get_omantel_block_value(
                block, "Int’l Minutes"))

            try:
                data_tag = block.select_one("p.Body-2.text-center")
                data["data_allowance"] = self.split_value_and_unit(
                    data_tag.text)
            except:
                data["data_allowance"] = self.split_value_and_unit(self.get_omantel_block_value(
                    block, "local & GCC"))

            data["world_roaming_data"] = self.split_value_and_unit(self.get_omantel_block_value(
                block, "World Roaming Data"))

            price_tag = block.select_one("div.price")
            data["price"] = self.split_value_and_unit(price_tag.text)

            if "OMR" in price_tag.text:
                data["price"]["unit"] = "OMR"

            if "month" in price_tag.text:
                data["duration"] = {"value": 1, "unit": "MONTH"}

            # data["data_sharing"] = self.get_omantel_block_value(
            #     package_div, "Data Sharing")
            # data["roaming_receiving_minutes"] = self.split_value_and_unit(self.get_omantel_block_value(
            #     package_div, "Roaming receiving minutes"))

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
