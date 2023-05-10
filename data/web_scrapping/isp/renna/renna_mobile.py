from data.web_scrapping.isp.renna.renna_toolkit import RennaToolkit
from utils.constants.common_data import common_data
from utils.package import Package


class RennaMobile(RennaToolkit):

    def __init__(self) -> None:
        super().__init__()
        self.soup = self.get_soup(self.RENNA_MOBILE_URL)
        self.packages = []
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select("tr")
        for index, block in enumerate(blocks):
            if any(w in block.text for w in ["Bundle Price", "(RO)"]):
                continue
            if "hidden" in block.parent.parent.parent.parent["class"]:
                continue

            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Renna Mobile",
                "link": self.RENNA_MOBILE_URL,
                "isp": "renna",
            })

            data["price"] = self.search_for_value(
                block, "td", ["ro", "bz"])

            data["data_allowance"] = self.search_for_value(
                block, "td", ["gb", "mb", "nonstop data"], type="data_allowance")

            data["duration"] = self.search_for_value(
                block, "td", ["hour", "day", "week"], type="duration")

            data["flexi_minutes"] = self.search_for_value(
                block, "td", ["min"], type="flexi_minutes")

            if not self.is_default(data["duration"]):
                package = Package(data)
                self.packages.append(package)
