from data.web_scrapping.isp.awaser.awaser_tookit import AwaserToolkit


class FiberHome(AwaserToolkit):

    def __init__(self):
        self.packages = []
        self.soup = self.get_soup(self.FIBER_HOME_URL)
        self.reset()
        self.get_packages()

    def get_packages(self):
        all_package_blocks = self.soup.select(
            "div.service-plan")
        for package_block in all_package_blocks:
            package = {"other": []}
            package["download_speed"] = self.get_download_speed(package_block)
            package["title"] = self.get_title(package_block)
            package["price"] = self.get_price(package_block)
            package["other"] = self.get_other(package_block)
            self.packages.append(package)

    def display(self):
        for package in self.packages:
            print(package)

    def reset(self):
        self.packages = []
