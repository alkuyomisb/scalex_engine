from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from domain.package import Package
from domain.constants.common_data import common_data


class OoredooHalaPlans(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.HALA_PLANS_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.plans__item")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Hala Plans",
                "link": self.HALA_PLANS_URL,
                "isp": "ooredoo",
                "add-ons": [
                    "https://www.ooredoo.om/Personal/Mobile/Hala(Prepaid)/HalaAdd-ons.aspx"
                ],
            })

            h5_tags = block.select("h5")
            for h5_tag in h5_tags:
                temp = h5_tag.text.strip()
                if self.str_to_data_allowance(temp)["value"] != 0:
                    data["data_allowance"] = self.str_to_data_allowance(temp)

            international_minutes_dict = self.get_ooredoo_block_value(
                block, "Local + Ind, Pak, Ban", split=True, value_tag="h5")

            data["international_minutes"] = international_minutes_dict["value"] if international_minutes_dict is not None else ""

            data["price"] = self.search_for_value(block, "h3", ["ro"])
            data["duration"] = self.str_to_duration(self.search_for_value(
                block, "span", ["day", "month", "week"], split=False))

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
