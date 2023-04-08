from data.web_scrapping.isp.redbull.redbull_toolkit import RedbullToolkit
from domain.package import Package
from domain.constants.common_data import common_data


class RedbullMobilePlans(RedbullToolkit):

    def __init__(self) -> None:
        super().__init__()
        self.packages = []
        self.soup = self.get_soup(self.MOBILE_PLANS_URL)
        self.get_packages()

    def get_packages(self):
        package_blocks = self.soup.select("div.home__card-inner")

        for block in package_blocks:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Redbull Mobile",
                "link": self.MOBILE_PLANS_URL,
                "isp": "redbull",

            })
            price = block.select_one(
                "div.home__card-title").text
            duration = block.select_one("div.home__card-date").text
            all_net_minutes = block.select_one("div.home__card-bonus").text
            included_data = block.select_one("div.home__card-capacity").text
            data["price"] = self.split_value_and_unit(price)
            data["data_allowance"] = self.split_value_and_unit(
                included_data)
            data["flexi_minutes"] = self.split_value_and_unit(
                all_net_minutes)['value']
            # data["all_net_minutes"] = self.split_value_and_unit(
            #     all_net_minutes)
            data["duration"] = self.split_value_and_unit(duration)
            data["isp"] = "redbull"

            package = Package(data)
            self.packages.append(package)
