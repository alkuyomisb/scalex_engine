from data.web_scrapping.isp.ooredoo.ooredoo_tookit import OoredooToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class OoredooSatelliteHomeInternet(OoredooToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.SATELLITE_HOME_INTERNET_URL)
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.plain-item")
        for block in blocks:
            data = common_data
            data.update({
                "service_type": "FIXED",
                "plan_type": "POSTPAID",
                "title": "Satellite Home Internet",
                "link": self.SATELLITE_HOME_INTERNET_URL,
                "isp": "ooredoo",

            })
            data["data_allowance"] = self.search_for_value(block, "li", ["gb"])
            data["price"] = self.search_for_value(block, "li", ["omr"])
            data["download_speed"] = self.search_for_value(
                block, "li", ["speed"])
            data["duration"] = self.str_to_duration(self.search_for_value(
                block, "span", ["monthly"], split=False))
            data["contract_duration"] = self.str_to_duration(self.search_for_value(
                block, "h2", ["contract"], split=False))

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
