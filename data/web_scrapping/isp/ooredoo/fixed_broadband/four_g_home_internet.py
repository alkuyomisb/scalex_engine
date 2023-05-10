from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class Ooredoo4GHomeInternet(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.FOUR_G_HOME_INTERNET_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.product-item")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "FIXED",
                "plan_type": "POSTPAID",
                "title": "4G Home Internet",
                "link": self.FOUR_G_HOME_INTERNET_URL,
                "isp": "ooredoo",

            })
            data["data_allowance"] = self.get_ooredoo_block_value(
                block,
                "internet",
                title_tag="div",
                value_tag="div",
                split=True,
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-lable.font-ooredoo.bold.text-cyan.text-display-medium"
            )
            data["download_speed"] = self.get_ooredoo_block_value(
                block,
                "speed",
                title_tag="div",
                value_tag="div",
                split=True,
                title_class_str=".product-lable",
                value_class_str=".product-lable.font-ooredoo.bold"
            )
            data["contract_duration"] = self.get_ooredoo_block_value(
                block,
                "CONTRACT",
                title_tag="div",
                value_tag="div",
                split=True,
                title_class_str=".product-lable",
                value_class_str=".product-value.font-ooredoo.bold.text-red.text-display-medium"
            )

            data["price"] = self.search_for_value(block, "span", ["omr"])
            data["duration"] = self.str_to_duration(self.search_for_value(
                block, "div", ["monthly"], split=False))

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
