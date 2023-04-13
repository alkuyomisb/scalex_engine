from data.web_scrapping.isp.friendly.friendly_toolkit import FriendlyToolkit
from utils.constants.common_data import common_data
from utils.package import Package
from utils.scalex_toolkit import get_soup


class FriendlyMobile(FriendlyToolkit):

    def __init__(self) -> None:
        super().__init__()
        self.soup = get_soup(self.FRIENDLY_MOBILE_URL)
        self.packages = []
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select("tr")
        for index, block in enumerate(blocks):
            if any(w in block.text for w in ["PRICE"]):
                continue

            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Freedom Plan",
                "link": self.FRIENDLY_MOBILE_URL,
                "isp": "friendly",
            })

            data["price"] = self.search_for_value(
                block, "td", ["ro", "bz"])

            data["data_allowance"] = self.search_for_value(
                block, "td", ["gb", "mb"], type="data_allowance")

            data["duration"] = self.search_for_value(
                block, "td", ["hour", "day", "week", "unlimited"], type="duration")

            data["flexi_minutes"] = self.search_for_value(
                block, "td", ["flexi"], type="flexi_minutes")

            data["local_minutes"] = self.search_for_value(
                block, "td", ["local"], type="local_minutes")

            package = Package(data)
            self.packages.append(package)
