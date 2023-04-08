from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from domain.package import Package
from domain.constants.common_data import common_data


class OoredooHalaSIM(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.HALA_SIM_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.shahry-postpaid-product__plans-item.plans__item")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Hala SIM",
                "link": self.HALA_SIM_URL,
                "isp": "ooredoo",
                "add-ons": [
                    "https://www.ooredoo.om/Personal/Mobile/Hala(Prepaid)/HalaAdd-ons.aspx"
                ],
            })

            international_minutes_dict = self.get_ooredoo_block_value(
                block, "International", split=True)
            data["international_minutes"] = international_minutes_dict["value"] if international_minutes_dict is not None else ""

            local_minutes_dict = self.get_ooredoo_block_value(
                block, "local", split=True, match_str=True)

            data["local_minutes"] = local_minutes_dict["value"] if local_minutes_dict is not None else ""

            data["data_allowance"] = self.get_ooredoo_block_value(
                block, "Local Data", split=True)

            span_tags = block.select("span")
            p_tags = block.select("p")
            for span in span_tags:
                if "RO" in span.text:
                    data["price"] = self.split_value_and_unit(span.text)

            for p in p_tags:
                if any(word in p.text.lower() for word in ["week", "month", "day"]):
                    data["duration"] = self.str_to_duration(p.text)

            if type(data["data_allowance"]) == dict:
                package = Package(data)
                self.packages.append(package)

    def reset(self):
        self.packages = []
