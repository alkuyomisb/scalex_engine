from data.web_scrapping.isp.omantel.omantel_tookit import OmantelToolkit


class OmantelBaqati(OmantelToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.NEW_BAQATI_URL)
        self.get_packages()

    def get_packages(self):
        package_divs = self.soup.select(
            "div._box._background-white")
        for package_div in package_divs:
            # self.output(package_div)
            package = {"other": []}
            self.get_omantel_package_title(package_div)
            package["local_minutes"] = self.get_omantel_block_value(
                package_div, "Local Minutes")
            package["international_minutes"] = self.split_value_and_unit(self.get_omantel_block_value(
                package_div, "Int’l Minutes"))
            package["roaming_receiving_minutes"] = self.split_value_and_unit(self.get_omantel_block_value(
                package_div, "Roaming receiving minutes"))
            package["world_roaming_data"] = self.split_value_and_unit(self.get_omantel_block_value(
                package_div, "World Roaming Data"))
            package["data_sharing"] = self.get_omantel_block_value(
                package_div, "Data Sharing")
            package["price"] = self.get_omantel_block_value(
                package_div, "month")
            package["other"].append(
                {"Discount - Gift Box": self.get_omantel_block_value(package_div, "Discount - Gift Box")})
            self.packages.append(package)

    def reset(self):
        self.packages = []
