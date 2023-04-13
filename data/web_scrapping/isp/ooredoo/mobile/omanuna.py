from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OoredooOmanuna(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.OMANUNA_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.shahry-postpaid-product__plans-item.plans__item")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "POSTPAID",
                "title": "Omanuna",
                "link": self.OMANUNA_URL,
                "duration": {"value": "1", "unit": "MONTH"},
                "isp": "ooredoo",

            })

            data["international_minutes"] = self.get_ooredoo_block_value(
                block, "International Voice")
            data["world_roaming"] = self.get_ooredoo_block_value(
                block, "World Roaming", split=True)

            span_tags = block.select("span")
            p_tags = block.select("p")
            for span in span_tags:
                if "RO" in span.text:
                    data["price"] = self.split_value_and_unit(span.text)

            for p in p_tags:
                if any(word in p.text for word in ["GB", "MB", "TB"]):
                    try:
                        p.span.decompose()
                        data["data_allowance"] = self.split_value_and_unit(
                            p.text)
                    except:
                        pass

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
