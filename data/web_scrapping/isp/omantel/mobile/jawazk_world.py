from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelJawazkWorld(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.JAWAZK_WORLD_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Jawazk World",
                "link": self.JAWAZK_WORLD_URL,
                "isp": "omantel",

            })

            content_tags = block.select("div._content")
            for index, content in enumerate(content_tags):
                if index == 0:
                    data["price"] = self.split_value_and_unit(content.text)
                elif index == 1:
                    data["data_allowance"] = self.split_value_and_unit(
                        content.text)
                elif index == 2:
                    data["flexi_minutes"] = self.split_value_and_unit(
                        content.text)
                elif index == 3:
                    data["duration"] = self.split_value_and_unit(content.text)

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
