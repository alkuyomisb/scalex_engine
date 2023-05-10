
from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OmantelTouristPacks(OmantelToolkit):
    packages = []

    def __init__(self):
        self.soup = self.get_soup(self.TOURIST_PACKS_URL)
        self.reset()
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div._box._background-white.pink")

        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Tourist Packs",
                "link": self.TOURIST_PACKS_URL,
                "isp": "omantel",
            })

            price_block = block.select_one(
                "h1.number.display-inline-block.margin-top-none.margin-bottom-none.baseline-fix.fz-48")
            price = self.split_value_and_unit(price_block.text)
            data["price"] = price

            data["data_allowance"] = self.get_omantel_block_value(
                block, "Allowance", split=True)

            data["duration"] = self.get_omantel_block_value(
                block, "Validity", split=True)

            minutes_sms_text = self.get_omantel_block_value(
                block, "Local and International", split=False)
            minutes = self.find_number(minutes_sms_text, ["min"])
            sms = self.find_number(minutes_sms_text, ["sms"])
            data["flexi_minutes"] = minutes
            data["sms"] = sms
            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
