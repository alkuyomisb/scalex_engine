
from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelAmanPlan(OmantelToolkit):
    packages = []

    def __init__(self):
        self.soup = self.get_soup(self.AMAN_PAN)
        self.reset()
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white.pink")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "POSTPAID",
                "title": "Aman Plan",
                "link": self.AMAN_PAN,
                "isp": "omantel",
            })

            price_tag = block.select_one("h6.fw-bold")
            data["price"] = self.split_value_and_unit(price_tag.text)
            data["data_allowance"] = self.get_omantel_block_value(
                block, "Data Allowance", split=True)
            social_media_data = self.get_omantel_block_value(
                block, "social media", split=True)
            data["social_media_data"] = social_media_data if social_media_data is not None else {
                "value": 0, "unit": "GB"}
            data["flexi_minutes"] = self.get_omantel_block_value(
                block, "Flexi Min")
            duration_tags = block.select("div._content.middle")
            data["duration"] = self.split_value_and_unit(
                duration_tags[len(duration_tags) - 1].text)

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
