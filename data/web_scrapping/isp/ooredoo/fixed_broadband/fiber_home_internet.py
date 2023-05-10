from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OoredooFiberHomeInternet(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.FIBER_HOME_INTERNET_URL)
        self.get_packages()

    def get_packages(self):
        contract = self.search_for_value(
            self.soup, "li", ["12-month contracts"], split=False)
        if contract != None:
            contract = {"value": 12, "unit": "MONTH"}
        else:
            contract = {"value": 0, "unit": ""}

        blocks = self.soup.select(
            "div.product-item")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "FIXED",
                "plan_type": "POSTPAID",
                "title": "5G Home Internet",
                "link": self.FIBER_HOME_INTERNET_URL,
                "isp": "ooredoo",

            })

            data["download_speed"] = self.get_ooredoo_block_value(
                block,
                "speed",
                title_tag="div",
                value_tag="div",
                split=True,
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-value.font-ooredoo.bold"
            )
            data["data_allowance"] = self.str_to_data_allowance(self.get_ooredoo_block_value(
                block,
                "LOCAL INTERNET",
                title_tag="div",
                value_tag="div",
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-value.font-ooredoo.bold"
            ))
            data["fixed_line_minutes"] = self.get_ooredoo_block_value(
                block,
                "LOCAL VOICE",
                title_tag="div",
                value_tag="div",
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-value.font-ooredoo.bold"
            )

            data["price"] = self.str_to_price(self.get_ooredoo_block_value(
                block,
                "PAY",
                title_tag="div",
                value_tag="div",
                split=False,
                title_class_str=".product-lable.bold.text-dark",
                value_class_str=".product-value.font-ooredoo.bold"
            ), order="UV")

            data["duration"] = self.str_to_duration(self.search_for_value(
                block, "div", ["pay"], split=False))
            data["contract_duration"] = contract

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
