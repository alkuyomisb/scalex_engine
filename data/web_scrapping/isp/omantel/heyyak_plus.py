
from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit
from domain.package import Package


class OmantelHeyyakPlus(OmantelToolkit):
    packages = []

    def __init__(self):
        self.soup = self.get_soup(self.HEYYAK_PLUS_URL)
        self.reset()
        self.get_packages()

    # This function will webscrap all the packages from the URL one by one.
    # Each package will be represented as a dictonary then adding them all the main list "self.packages".
    def get_packages(self):
        package_divs = self.soup.select(
            "div._box._background-white.pink")
        for package_div in package_divs:
            data = {
                "price": "",
                "data_allowance": "",
                "flexi_minutes": "",
                "local_minutes": 0,
                "international_minutes": 0,
                "social_media_data": {"value": 0, "unit": "GB"},
                "duration": "",
                "link": self.HEYYAK_PLUS_URL,
                "isp": "omantel",
            }
            # WebScrap Price
            price_tag = package_div.select_one("h6.fw-bold")
            data["price"] = self.split_value_and_unit(price_tag.text)

            # WebScrap "Duration"
            duration_tag = package_div.select_one("h1.number")
            duration_title_tag = package_div.select_one(
                "sup.display-inline-block")
            duration = {
                "value": duration_tag.text,
                "unit": self.clear_string(duration_title_tag.text),
            }

            data["duration"] = duration

            data["data_allowance"] = self.get_omantel_block_value(
                package_div, "Data Allowance", split=True)

            data["social_media_data"] = self.get_omantel_block_value(
                package_div, "Social Media Data", split=True)

            data["flexi_minutes"] = self.get_omantel_block_value(
                package_div, "Flexi Minutes")

            package = Package(data)
         

            self.packages.append(package)

    def reset(self):
        self.packages = []
