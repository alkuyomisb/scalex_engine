
from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from domain.package import Package
from domain.constants.common_data import common_data


class OmantelHeyyakDataOnly(OmantelToolkit):
    packages = []

    def __init__(self):
        self.soup = self.get_soup(self.DATA_ONLY_URL)
        self.reset()
        self.get_packages()

    # This function will webscrap all the packages from the URL one by one.
    # Each package will be represented as a dictonary then adding them all the main list "self.packages".
    def get_packages(self):
        package_divs = self.soup.select(
            "div._box._background-white.Black")
        for package_div in package_divs:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "POSTPAID",
                "title": "Data Only Plan",
                "link": self.DATA_ONLY_URL,
                "isp": "omantel",
            })
            # WebScrap Price
            price_tag = package_div.select_one("h6.fw-bold")
            data["price"] = self.split_value_and_unit(price_tag.text)
            duration_tags = package_div.select("div._content.middle")
            data["duration"] = self.split_value_and_unit(
                duration_tags[len(duration_tags) - 1].text)
            data["data_allowance"] = self.get_omantel_block_value(
                package_div, "Data Allowance", split=True)

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
