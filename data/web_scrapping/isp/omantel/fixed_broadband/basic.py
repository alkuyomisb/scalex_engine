from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelBasic(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.BASIC_URL)
        self.get_packages()

    def get_packages(self):
        package_divs = self.soup.select(
            "div._box._background-white")
        for package_div in package_divs:
            data = common_data.copy()
            data.update({
                "service_type": "FIXED",
                "plan_type": "POSTPAID",
                "title": "Basic",
                "link": self.BASIC_URL,
                "isp": "omantel",
            })

            data["download_speed"] = self.get_omantel_block_value(
                package_div, "Download speed", split=True)
            data["upload_speed"] = self.get_omantel_block_value(
                package_div, "Upload speed", split=True)
            data["fixed_line_minutes"] = self.get_omantel_block_value(
                package_div, "Fixed Lines", split=False)

            data["data_allowance"] = self.get_omantel_block_value(
                package_div, "Data included", split=True)

            price_tag = package_div.select_one("div.price")
            data["price"] = self.split_value_and_unit(price_tag.text)
            if "OMR" in price_tag.text:
                data["price"]["unit"] = "OMR"

            if "month" in price_tag.text:
                data["duration"] = {"value": 1, "unit": "MONTH"}

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
