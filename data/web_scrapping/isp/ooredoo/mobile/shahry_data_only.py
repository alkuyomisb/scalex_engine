from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OoredooShahryDataOnly(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.SHAHRY_DATA_ONLY_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.shahry-postpaid-product__plans-item.plans__item")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "POSTPAID",
                "title": "Shahry Data Only",
                "link": self.SHAHRY_DATA_ONLY_URL,
                "isp": "ooredoo",

            })

            span_tags = block.select("span")
            p_tags = block.select("p")
            for span in span_tags:
                if "RO" in span.text:
                    data["price"] = self.split_value_and_unit(span.text)

            for p in p_tags:
                if any(word in p.text for word in ["GB", "MB"]):
                    data["data_allowance"] = self.split_value_and_unit(
                        p.text)
                elif "Unlimited" in p.text:
                    data["data_allowance"] = "unlimited"
                elif "30 days" in p.text:
                    data["duration"] = {"value": "1", "unit": "MONTH"}

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
