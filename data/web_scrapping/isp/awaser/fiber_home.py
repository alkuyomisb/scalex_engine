from data.web_scrapping.isp.awaser.awaser_tookit import AwaserToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class FiberHome(AwaserToolkit):

    def __init__(self):
        self.packages = []
        self.soup = self.get_soup(self.FIBER_HOME_URL)
        self.reset()
        self.get_packages()

    def get_packages(self):
        blocks = self.soup.select(
            "div.service-plan")
        for block in blocks:
            data = common_data.copy()
            data.update({
                "service_type": "FIXED",
                "plan_type": "POSTPAID",
                "title": "Fiber Home",
                "link": self.FIBER_HOME_URL,
                "isp": "awasr",
                "contract_duration": {"value": 12, "unit": "MONTH"},
                "duration": {"value": 1, "unit": "MONTH"},
            })

            data["download_speed"] = self.get_download_speed(block)
            data["price"] = self.get_price(block)

            data["data_allowance"] = self.search_for_value(
                block, "li", ["unlimited data"], type="data_allowance")

            other = self.get_other(block)
            upload_speed_text = [
                item for item in other if "upload speed" in item.lower()][0]
            upload_speed = {
                "value": self.extract_number(upload_speed_text, data_type="float"),
                "unit": "MBPS"
            }
            data["upload_speed"] = upload_speed

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
