from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OoredooTouristPlans(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.TOURIST_PLANS_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.product-item-wrapper")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Tourist Plans",
                "link": self.TOURIST_PLANS_URL,
                "isp": "ooredoo",

            })

            data["sms"] = self.get_ooredoo_block_value(
                block,
                "SMS",
                split=True,
                title_tag="div",
                value_tag="div",
                title_class_str=".product-info-lable.font-ooredoo.bold.text-red",
                value_class_str=".product-value.font-ooredoo.bold.text-cyan")["value"]

            data["data_allowance"] = self.get_ooredoo_block_value(
                block,
                "INTERNET *",
                split=True,
                title_tag="div",
                value_tag="div",
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-value.font-ooredoo.bold.text-cyan")

            data["international_minutes"] = self.get_ooredoo_block_value(
                block,
                "minutes",
                split=True,
                title_tag="div",
                value_tag="div",
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-value.font-ooredoo.bold.text-red")["value"]

            data["world_roaming"] = self.get_ooredoo_block_value(
                block,
                "Local/Roaming in Qatar",
                split=True,
                title_tag="small",
                value_tag="div",
                value_class_str=".product-value.font-ooredoo.bold.text-cyan")

            data["price"] = self.search_for_value(block, "h2", ["omr"])
            data["duration"] = self.str_to_duration(self.search_for_value(
                block, "div", ["day", "month", "week"], split=False))

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
