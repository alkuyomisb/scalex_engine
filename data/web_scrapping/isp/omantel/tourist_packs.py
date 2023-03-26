
from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit


class TouristPacks(OmantelToolkit):
    packages = []

    def __init__(self):
        self.soup = self.get_soup(self.TOURIST_PACKS_URL)
        self.reset()
        self.get_packages()

    # This function will webscrap all the packages from the URL one by one.
    # Each package will be represented as a dictonary then adding them all the main list "self.packages".

    def get_packages(self):
        package_divs = self.soup.select(
            "div._box._background-white.pink")

        for package_div in package_divs:
            package = {"other": [], "duration": ""}
            price_block = package_div.select_one(
                "h1.number.display-inline-block.margin-top-none.margin-bottom-none.baseline-fix.fz-48")
            price = self.split_value_and_unit(price_block.text)
            package["price"] = price
            package["data_allowance"] = self.get_omantel_block_value(
                package_div, "Allowance", split=True)
            package["other"].append(
                {"Welcome Bonus": self.get_omantel_block_value(package_div, "Welcome Bonus", split=True)})
            package["duration"] = self.get_omantel_block_value(
                package_div, "Validity", split=True)
            package["other"].append(
                {"O-Taxi Free trip": self.get_omantel_block_value(package_div, "O-Taxi Free trip", split=True)})
            package["other"].append(
                {"calls within Tourist Packs": self.get_omantel_block_value(package_div, "calls within Tourist Packs")})
            package["other"].append(
                {"Local and International": self.get_omantel_block_value(package_div, "Local and International")})

            self.packages.append(package)

    def reset(self):
        self.packages = []
