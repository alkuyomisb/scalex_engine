
from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from domain.package import Package
from domain.constants.common_data import common_data


class OmantelHeyyakPlus(OmantelToolkit):
    packages = []

    def __init__(self):
        self.soup = self.get_soup(self.HEYYAK_PLUS_URL)
        self.reset()
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white.pink")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Hayyak Plus",
                "link": self.HEYYAK_PLUS_URL,
                "isp": "omantel",
                "add-ons": [
                    " https://www.omantel.om/Personal/mobile/hayyak/Hayyak-Plus/Add-ons/erada"
                ]
            })

            price_tag = block.select_one("h6.fw-bold")
            data["price"] = self.split_value_and_unit(price_tag.text)

            duration_tag = block.select_one("h1.number")
            duration_title_tag = block.select_one(
                "sup.display-inline-block")
            duration = {
                "value": duration_tag.text if len(duration_tag.text) > 0 else 0,
                "unit": self.clear_string(duration_title_tag.text),
            }
            if duration["unit"] == "weekly":
                duration["unit"] = "DAY"
                duration["value"] = 7
            else:
                duration = self.unify_unit(duration)

            data["duration"] = duration

            data["data_allowance"] = self.get_omantel_block_value(
                block, "Data Allowance", split=True)

            data["social_media_data"] = self.get_omantel_block_value(
                block, "Social Media Data", split=True)

            data["flexi_minutes"] = self.get_omantel_block_value(
                block, "Flexi Minutes") if self.get_omantel_block_value(
                block, "Flexi Minutes") is not None else 0

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
